#!/usr/in/env python
import abc

from hebrew import Hebrew
from hebrew.chars import NiqqudChar


class BaseFixer(abc.ABC):
    DAGESH = NiqqudChar.search("DAGESH").char
    SHEVA = NiqqudChar.search("SHEVA").char

    @abc.abstractmethod
    def fix(self, word: str) -> str:
        ...

    def _get_graphemes(self, word: str) -> list[str]:
        hebrew_word = Hebrew(word)
        try:
            return [str(g) for g in hebrew_word.graphemes]
        except:
            print(word)

    def _has_dagesh(self, grapheme: str) -> bool:
        return self.DAGESH in grapheme

    def _has_sheva(self, grapheme: str) -> bool:
        return self.SHEVA in grapheme


