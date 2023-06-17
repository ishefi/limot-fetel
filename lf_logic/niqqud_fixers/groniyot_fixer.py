#!/usr/in/env python
from hebrew.chars import NiqqudChar

from lf_logic.niqqud_fixers.base_fixer import BaseFixer


class GroniyotFixer(BaseFixer):
    GRONIYOT = 'אהחער'
    HATAF_PATAX = NiqqudChar.search("HATAF PATAH").char

    def fix(self, word):
        graphemes = self._get_graphemes(word)
        for i, grapheme in enumerate(graphemes):
            if not self._is_gronit(grapheme):
                continue
            if self._has_sheva(grapheme):
                graphemes[i] = self._haxtef(grapheme)
            if self._has_dagesh(grapheme):
                graphemes[i] = self._remove_dagesh(grapheme)
        return ''.join(graphemes)

    def _is_gronit(self, grapheme: str) -> bool:
        for char in self.GRONIYOT:
            if char in grapheme:
                return True
        return False

    def _remove_dagesh(self, grapheme: str) -> str:
        return grapheme.replace(self.DAGESH, '')

    def _haxtef(self, grapheme: str) -> str:
        # TOOD: implement based on jb-jd here:
        # https://hebrew-academy.org.il/topic/hahlatot/grammardecisions/netiyyat-hapoal/3-2-%D7%94%D7%A4%D7%95%D7%A2%D7%9C-%D7%91%D7%A9%D7%95%D7%A8%D7%A9%D7%99%D7%9D-%D7%91%D7%A2%D7%9C%D7%99-%D7%A2%D7%99%D7%A6%D7%95%D7%A8%D7%99%D7%9D-%D7%92%D7%A8%D7%95%D7%A0%D7%99%D7%99%D7%9D/#target-3120
        return grapheme.replace(self.SHEVA, self.HATAF_PATAX)
