#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import random
from typing import TYPE_CHECKING

import milon.dictionaries
from pydantic import BaseModel

from lf_logic.consts import WEIGHTS

if TYPE_CHECKING:
    from typing import Optional


class Root(BaseModel):
    p: str
    a: str
    l: str


class GeneratorLogic:
    CHARS = 'אבגדהוזחטיכלמנסעפצקרשת'
    LAST_LETTERS = {
        "מ": "ם",
        "נ": "ן",
        "צ": "ץ",
        "פ": "ף",
        "כ": "ך",
    }

    def __init__(self):
        self.milon = milon.dictionaries.DictionaryHeEn(limit=0)
        self.milon_words = [
            word['translated'] for word in self.milon.words
        ]

    async def generate(self, num_of_roots=10):
        roots = [self._gen_random_root() for _ in range(num_of_roots)]
        potential_nons = []

        for root in roots:
            potential_nons += random.choices([
                weight.replace('ק', root.p).replace('ט', root.a).replace('ל', root.l)
                for weight in WEIGHTS
            ], k=10)
        nons = asyncio.gather(
            *[self._filter_nonword(word) for word in potential_nons]
        )

        return [non for non in await nons if non is not None]

    def _gen_random_root(self) -> Root:
        return Root(
            p=random.choice(self.CHARS),
            a=random.choice(self.CHARS),
            l=random.choice(self.CHARS),
        )

    async def _filter_nonword(self, word: str) -> Optional[str]:
        if word in self.milon_words:
            return None
        else:
            return self._fix_last_letter(word)

    def _fix_last_letter(self, word: str) -> str:
        last_letter = word[-1]
        replacement = self.LAST_LETTERS.get(last_letter, word[-1])
        return word[:-1] + replacement
