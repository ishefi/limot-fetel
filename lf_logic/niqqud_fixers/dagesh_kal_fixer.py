#!/usr/in/env python
# -*- coding: utf-8 -*-
from lf_logic.niqqud_fixers.base_fixer import BaseFixer


class DageshKalFixer(BaseFixer):
    BEGED_KEFET = "בגדכפת"

    @staticmethod
    def fix(word):
        graphemes = DageshKalFixer._get_graphemes(word)
        after_tnua = False
        for i, grapheme in enumerate(graphemes):
            is_beged_kefet = DageshKalFixer._is_beged_kefet(grapheme)
            has_dagesh = DageshKalFixer._has_dagesh(grapheme)
            if is_beged_kefet and not has_dagesh and not after_tnua:
                graphemes[i] = grapheme + DageshKalFixer.DAGESH
            after_tnua = DageshKalFixer._has_tnua(grapheme)
        return "".join(graphemes)

    @staticmethod
    def _is_beged_kefet(grapheme) -> bool:
        for char in DageshKalFixer.BEGED_KEFET:
            if char in grapheme:
                return True
        return False

    @staticmethod
    def _has_tnua(grapheme) -> bool:
        return not DageshKalFixer._has_sheva(
            grapheme
        )  # TODO: this doesn't account for sheva-na
