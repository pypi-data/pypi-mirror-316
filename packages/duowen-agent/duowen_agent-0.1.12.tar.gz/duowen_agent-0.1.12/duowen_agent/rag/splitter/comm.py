import re
from typing import List

from duowen_agent.rag.models import Document


def split_text_with_regex(
    text: str, separator: str = "\n\n", keep_separator: bool = True
) -> list[str]:
    # Now that we have the separator, split the text
    if separator:
        if keep_separator:
            # The parentheses in the pattern keep the delimiters in the result.
            _splits = re.split(f"({re.escape(separator)})", text)
            splits = [_splits[i - 1] + _splits[i] for i in range(1, len(_splits), 2)]
            if len(_splits) % 2 != 0:
                splits += _splits[-1:]
        else:
            splits = re.split(separator, text)
    else:
        splits = list(text)
    return [s for s in splits if (s not in {"", "\n"})]


def merge_document(docs: List[Document]): ...
