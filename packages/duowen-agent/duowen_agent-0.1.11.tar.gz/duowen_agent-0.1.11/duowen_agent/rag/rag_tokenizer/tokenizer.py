import re
import threading
from typing import Optional, List, Dict

import nltk
from hanziconv import HanziConv
from jieba import Tokenizer
from jieba.analyse import TFIDF, TextRank
from jieba.posseg import POSTokenizer
from nltk import word_tokenize
from nltk.data import find
from nltk.stem import PorterStemmer, WordNetLemmatizer
from rake_nltk import Rake

from .stopwords import STOPWORDS


# nltk.download("punkt")
# nltk.download("stopwords")


def ensure_nltk_resource(resource_name):
    try:
        # 检查资源是否存在
        find(resource_name)
    except LookupError:
        # 如果资源不存在，则下载
        print(f"Resource '{resource_name}' not found. Downloading...")
        nltk.download(resource_name)


ensure_nltk_resource("punkt")
ensure_nltk_resource("stopwords")


def is_chinese(s) -> bool:
    if "\u4e00" <= s <= "\u9fa5":
        return True
    else:
        return False


def is_number(s) -> bool:
    if "\u0030" <= s <= "\u0039":
        return True
    else:
        return False


def is_alphabet(s) -> bool:
    if ("\u0041" <= s <= "\u005a") or ("\u0061" <= s <= "\u007a"):
        return True
    else:
        return False


def full_to_half_width(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xFEE0
        if (
            inside_code < 0x0020 or inside_code > 0x7E
        ):  # 转完之后不是半角字符返回原来的字符
            rstring += uchar
        else:
            rstring += chr(inside_code)
    return rstring


def traditional_to_simplified(line):
    """繁体转简体"""
    return HanziConv.toSimplified(line)


class RagTokenizer:
    def __init__(
        self,
        min_keywords_upper_limit: int = 10,
        max_keywords_upper_limit: int = None,
        ratio: float = 0.02,
        pos_filt: List[str] = None,
    ):
        """
        :param ratio: Ratio for topK estimation based on text length.
        :param min_keywords_upper_limit: Maximum limit for topK.

        """

        self.stopwords = STOPWORDS.copy()
        self.tokenizer = Tokenizer()
        self.pos_tokenizer = POSTokenizer(self.tokenizer)
        self.tfidf = TFIDF()
        self.textrank = TextRank()
        self.textrank.tokenizer = self.pos_tokenizer
        self.textrank.stop_words = self.stopwords
        if pos_filt:
            self.textrank.pos_filt = frozenset(pos_filt)
        else:
            self.textrank.pos_filt = frozenset(
                ("n", "nz", "nr", "nrt", "ns", "nt", "v", "vn", "j", "t", "i")
            )
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

        self.min_keywords_upper_limit = min_keywords_upper_limit
        self.max_keywords_upper_limit = (
            max_keywords_upper_limit if max_keywords_upper_limit else 999999999
        )
        self.ratio = ratio

    def add_stopword(self, word: str):
        """添加停词"""
        self.stopwords.add(word)

    def add_word(self, word, frequency: int = None, pos: str = None):
        """添加词性标注"""
        self.tokenizer.add_word(word, frequency, pos)

    def extract_keywords_tfidf(
        self, text: str, max_keywords_per_chunk: Optional[int] = 10
    ) -> List[str]:
        keywords = self.tfidf.extract_tags(text, max_keywords_per_chunk)
        data = []
        for i in keywords:
            data.extend(self.tokenizer.lcut_for_search(i))
        return data

    def extract_keywords_textrank(
        self, text: str, max_keywords_per_chunk: Optional[int] = 10
    ) -> List[str]:
        keywords = self.textrank.textrank(sentence=text, topK=max_keywords_per_chunk)
        data = []
        for i in keywords:
            data.extend(self.tokenizer.lcut_for_search(i))
        return data

    @staticmethod
    def preprocess_text(text: str) -> str:
        line = full_to_half_width(text).lower()
        line = traditional_to_simplified(line)
        return line

    def _estimate_topk_cn(self, text: str) -> int:
        effective_length = len(re.findall(r"[\u4e00-\u9fa5]", text))
        estimated_topk = int(effective_length * self.ratio)

        return max(
            self.min_keywords_upper_limit,
            min(estimated_topk, self.max_keywords_upper_limit),
        )

    def _estimate_topk_en(self, text: str) -> int:
        effective_length = len(re.findall(r"[a-zA-Z0-9]+", text))
        estimated_topk = int(effective_length * self.ratio)
        return max(
            self.min_keywords_upper_limit,
            min(estimated_topk, self.max_keywords_upper_limit),
        )

    @staticmethod
    def extract_eng(text: str) -> str:
        return re.sub(r"[^a-zA-Z]", " ", text).strip()

    def extract_eng_keywords(self, text: str) -> List[str]:
        _r = Rake(max_length=self._estimate_topk_en(text))
        _r.extract_keywords_from_text(text)
        data = []
        for line in _r.get_ranked_phrases():
            data.append(
                "_".join(
                    [
                        self.stemmer.stem(self.lemmatizer.lemmatize(t))  # 词形转换
                        for t in word_tokenize(line)
                    ]
                )
            )
        return data

    def extract_keywords(self, text, mode="textrank") -> set[str]:

        _text = self.preprocess_text(text)
        zh_num = len([1 for c in _text if is_chinese(c)])
        if zh_num == 0:
            return set(self.extract_eng_keywords(_text))

        if mode == "tfidf":
            _data = self.extract_keywords_tfidf(_text, self._estimate_topk_cn(_text))

        elif mode == "textrank":
            _data = self.extract_keywords_textrank(_text, self._estimate_topk_cn(_text))
        else:
            raise ValueError(f"RagTokenizer.extract_keywords Unsupported mode: {mode}")

        _en_data = self.extract_eng(_text)

        if _en_data:
            return set(_data + self.extract_eng_keywords(_en_data))
        else:
            return set(_data)


class RagTokenizerWrapper:

    def __init__(self):
        self.rag_tokenizer_instance: Dict[str, RagTokenizer] = {}
        self.lock = threading.Lock()

    def get_instance(self, item: str):
        with self.lock:
            if item not in self.rag_tokenizer_instance:
                self.rag_tokenizer_instance[item] = RagTokenizer()
            return self.rag_tokenizer_instance[item]


rag_tokenizers = RagTokenizerWrapper()
