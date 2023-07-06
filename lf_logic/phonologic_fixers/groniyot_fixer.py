#!/usr/in/env python
# -*- coding: utf-8 -*-

from lf_logic.phonologic_fixers.base_fixer import BaseFixer


class GroniyotFixer(BaseFixer):
    GRONIYOT = "אהחער"
    HATAF_PATAX = "ֲ"

    @staticmethod
    def fix(word):
        graphemes = GroniyotFixer._get_graphemes(word)
        for i, grapheme in enumerate(graphemes):
            if not GroniyotFixer._is_gronit(grapheme):
                continue
            if GroniyotFixer._has_sheva(grapheme):
                graphemes[i] = grapheme = GroniyotFixer._haxtef(grapheme)
            if GroniyotFixer._has_dagesh(grapheme):
                graphemes[i] = GroniyotFixer._remove_dagesh(grapheme)
        return "".join(graphemes)

    @staticmethod
    def _is_gronit(grapheme: str) -> bool:
        for char in GroniyotFixer.GRONIYOT:
            if char in grapheme:
                return True
        return False

    @staticmethod
    def _remove_dagesh(grapheme: str) -> str:
        return grapheme.replace(GroniyotFixer.DAGESH, "")

    @staticmethod
    def _haxtef(grapheme: str) -> str:
        # TOOD: implement based on jb-jd here:
        # https://hebrew-academy.org.il/topic/hahlatot/grammardecisions/netiyyat-hapoal/3-2-%D7%94%D7%A4%D7%95%D7%A2%D7%9C-%D7%91%D7%A9%D7%95%D7%A8%D7%A9%D7%99%D7%9D-%D7%91%D7%A2%D7%9C%D7%99-%D7%A2%D7%99%D7%A6%D7%95%D7%A8%D7%99%D7%9D-%D7%92%D7%A8%D7%95%D7%A0%D7%99%D7%99%D7%9D/#target-3120
        return grapheme.replace(GroniyotFixer.SHEVA, GroniyotFixer.HATAF_PATAX)
