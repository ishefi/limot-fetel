#!/usr/in/env python
from lf_logic.niqqud_fixers.base_fixer import BaseFixer


class DageshKalFixer(BaseFixer):
    BEGED_KEFET = 'בגדכפת'

    def fix(self, word):
        graphemes = self._get_graphemes(word)
        after_tnua = False
        for i, grapheme in enumerate(graphemes):
            is_beged_kefet = self._is_beged_kefet(grapheme)
            has_dagesh = self._has_dagesh(grapheme)
            if is_beged_kefet and not has_dagesh and not after_tnua:
                graphemes[i] = grapheme + self.DAGESH
            after_tnua = self._has_tnua(grapheme)
        return ''.join(graphemes)

    def _is_beged_kefet(self, grapheme) -> bool:
        for char in self.BEGED_KEFET:
            if char in grapheme:
                return True
        return False

    def _has_tnua(self, grapheme) -> bool:
        return not self._has_sheva(grapheme)  # TODO: this doesn't account for sheva-na
