#!/usr/in/env python
# -*- coding: utf-8 -*-
from lf_base import schemas
from lf_logic.phonologic_fixers.base_fixer import BaseFixer


class HitpaelFixer(BaseFixer):
    ORDER = 25
    TEMPLATE = "הִתְפַעֵּל"
    VOICE_ASSIM = {"ז": "ד"}
    EMPATHIC_ASSIM = {"צ": "ט"}

    SIBILANTS = "זסצש"

    @staticmethod
    def fix(word: schemas.NonWord) -> None:
        if word.template != HitpaelFixer.TEMPLATE:
            return
        root_p, _, _ = word.root.split("-")
        if root_p not in HitpaelFixer.SIBILANTS:
            return
        h, t, p, a, el = HitpaelFixer._get_graphemes(word.populated)
        t_replacer = HitpaelFixer._get_t_replacer(root_p)
        word.populated = "".join(
            [h, t.replace("ת", root_p), p.replace(root_p, t_replacer), a, el]
        )

    @staticmethod
    def _get_t_replacer(pe: str) -> str:
        if pe in HitpaelFixer.EMPATHIC_ASSIM:
            return HitpaelFixer.EMPATHIC_ASSIM[pe]
        elif pe in HitpaelFixer.VOICE_ASSIM:
            return HitpaelFixer.VOICE_ASSIM[pe]
        else:
            return "ת"
