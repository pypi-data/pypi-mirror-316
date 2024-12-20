import re
from bisect import bisect_left
from itertools import accumulate
from typing import Callable

from duowen_agent.rag.models import Document


class RecursiveChunker:
    """移植 https://github.com/umarbutler/semchunk"""

    def __init__(
        self,
        NON_WHITESPACE_SEMANTIC_SPLITTERS: tuple[str] = None,
        str_len: Callable[[str], int] = None,
    ):
        if NON_WHITESPACE_SEMANTIC_SPLITTERS is None:
            self.NON_WHITESPACE_SEMANTIC_SPLITTERS = ("。", "？", "！", ".", "?", "!")

        else:
            self.NON_WHITESPACE_SEMANTIC_SPLITTER = NON_WHITESPACE_SEMANTIC_SPLITTERS

        if str_len:
            self._str_len = str_len
        else:
            self._str_len = len

    def _split_text(self, text: str) -> tuple[str, bool, list[str]]:
        """Split text using the most semantically meaningful splitter possible."""

        splitter_is_whitespace = True

        if "\n" in text or "\r" in text:
            splitter = max(re.findall(r"[\r\n]+", text))

        elif "\t" in text:
            splitter = max(re.findall(r"\t+", text))

        elif re.search(r"\s", text):
            splitter = max(re.findall(r"\s+", text))

        else:
            # Identify the most desirable semantically meaningful non-whitespace splitter present in the text.
            for splitter in self.NON_WHITESPACE_SEMANTIC_SPLITTERS:
                if splitter in text:
                    splitter_is_whitespace = False
                    break

            # If no semantically meaningful splitter is present in the text, return an empty string as the splitter and the text as a list of characters.
            else:  # NOTE This code block will only be executed if the for loop completes without breaking.
                return "", splitter_is_whitespace, list(text)

        # Return the splitter and the split text.
        return splitter, splitter_is_whitespace, text.split(splitter)

    @staticmethod
    def merge_splits(
        self, splits: list[str], chunk_size: int, splitter: str
    ) -> tuple[int, str]:
        """Merge splits until a chunk size is reached, returning the index of the last split included in the merged chunk along with the merged chunk itself."""

        average = 0.2
        low = 0
        high = len(splits) + 1
        cumulative_lengths = list(
            accumulate([len(split) for split in splits], initial=0)
        )
        cumulative_lengths.append(cumulative_lengths[-1])

        while low < high:
            i = bisect_left(cumulative_lengths[low : high + 1], chunk_size * average)
            midpoint = min(i + low, high - 1)

            tokens = self._str_len(splitter.join(splits[:midpoint]))

            average = (
                cumulative_lengths[midpoint] / tokens
                if cumulative_lengths[midpoint] and tokens > 0
                else average
            )

            if tokens > chunk_size:
                high = midpoint
            else:
                low = midpoint + 1

        return low - 1, splitter.join(splits[: low - 1])

    def chunk(
        self,
        text: str,
        chunk_size: int = 1000,
        memoize: bool = True,
        _recursion_depth: int = 0,
        _reattach_whitespace_splitters: bool = False,
    ) -> list[str]:
        """Split a text into semantically meaningful chunks of a specified size as determined by the provided token counter.

        Args:
            text (str): The text to be chunked.
            chunk_size (int): The maximum number of tokens a chunk may contain.
            token_counter (Callable[[str], int]): A callable that takes a string and returns the number of tokens in it.
            memoize (bool, optional): Whether to memoize the token counter. Defaults to `True`.

        Returns:
            list[str]: A list of chunks up to `chunk_size`-tokens-long, with any whitespace used to split the text removed.
        """

        # If this is not a recursive call and memoization is enabled, overwrite the `token_counter` with a memoized version of itself.

        # Split the text using the most semantically meaningful splitter possible.
        splitter, splitter_is_whitespace, splits = self._split_text(text)
        if _reattach_whitespace_splitters:
            splitter_is_whitespace = False

        chunks = []
        skips = set()
        """A list of indices of splits to skip because they have already been added to a chunk."""

        # Iterate through the splits.
        for i, split in enumerate(splits):
            # Skip the split if it has already been added to a chunk.
            if i in skips:
                continue

            # If the split is over the chunk size, recursively chunk it.
            if self._str_len(split) > chunk_size:
                chunks.extend(
                    self.chunk(
                        split,
                        chunk_size,
                        memoize=memoize,
                        _recursion_depth=_recursion_depth + 1,
                        _reattach_whitespace_splitters=_reattach_whitespace_splitters,
                    )
                )

            # If the split is equal to or under the chunk size, add it and any subsequent splits to a new chunk until the chunk size is reached.
            else:
                # Merge the split with subsequent splits until the chunk size is reached.
                final_split_in_chunk_i, new_chunk = self.merge_splits(
                    splits[i:], chunk_size, splitter
                )

                # Mark any splits included in the new chunk for exclusion from future chunks.
                skips.update(range(i + 1, i + final_split_in_chunk_i))

                # Add the chunk.
                chunks.append(new_chunk)

            # If the splitter is not whitespace and the split is not the last split, add the splitter to the end of the last chunk if doing so would not cause it to exceed the chunk size otherwise add the splitter as a new chunk.
            if not splitter_is_whitespace and not (
                i == len(splits) - 1
                or all(j in skips for j in range(i + 1, len(splits)))
            ):
                if (
                    self._str_len(last_chunk_with_splitter := chunks[-1] + splitter)
                    <= chunk_size
                ):
                    chunks[-1] = last_chunk_with_splitter
                else:
                    chunks.append(splitter)

        # If this is not a recursive call, remove any empty chunks.
        if not _recursion_depth:
            chunks = list(filter(None, chunks))

        return [
            Document(
                page_content=i,
                metadata={"chunk_index": index},
            )
            for index, i in enumerate(chunks)
        ]
