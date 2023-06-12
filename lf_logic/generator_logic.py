#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import random
import re
from typing import TYPE_CHECKING

import milon.dictionaries
from pydantic import BaseModel

from lf_logic import consts

if TYPE_CHECKING:
    from typing import Optional


class Root(BaseModel):
    p: str
    a: str
    l: str


class Template(BaseModel):
    root: Root
    template: str

    @staticmethod
    def noun_template(template):
        return Template(root=Root(p='ק', a='ט', l='ל'), template=template)

    @staticmethod
    def verb_template(template):
        return Template(root=Root(p='פ', a='ע', l='ל'), template=template)

    @property
    def root_regex(self):
        return f'({self.root.p})|({self.root.a})|({self.root.l})'


class GeneratorLogic:
    CHARS = 'אבגדהוזחטיכלמנסעפצקרשת'
    LAST_LETTERS = {
        "מ": "ם",
        "נ": "ן",
        "צ": "ץ",
        "פ": "ף",
        "כ": "ך",
    }

    def __init__(self, templates, weights):
        self.milon = milon.dictionaries.DictionaryHeEn(limit=0)
        self.milon_words = [
            word['translated'] for word in self.milon.words
        ]
        self.templates = templates or consts.VERB_TEMPLATES
        self.weights = weights or consts.WEIGHTS
        print(self.weights)

    async def generate(
            self, num_of_roots: int, p: str | None, a: str | None, l: str | None
    ):
        roots = [self._gen_random_root(p, a, l) for _ in range(num_of_roots)]
        potential_nons = []

        for root in roots:
            potential_nons += random.choices([
                self._populate_template(Template.noun_template(weight), root)
                for weight in self.weights
            ], k=10)
            potential_nons += [
                self._populate_template(Template.verb_template(template), root)
                for template in self.templates
            ]
        nons = asyncio.gather(
            *[self._filter_nonword(word) for word in potential_nons]
        )

        return [non for non in await nons if non is not None]

    def _populate_template(self, template: Template, root: Root):
        replacer_dict = {
            template.root.p: root.p, template.root.a: root.a, template.root.l: root.l

        }
        replacer = lambda match: replacer_dict[match.string[match.start(): match.end()]]
        return re.sub(template.root_regex, replacer, template.template)

    def _gen_random_root(self, p, a, l) -> Root:
        return Root(
            p=p or random.choice(self.CHARS),
            a=a or random.choice(self.CHARS),
            l=l or random.choice(self.CHARS),
        )

    async def _filter_nonword(self, word: str) -> str | None:
        if word in self.milon_words:
            return None
        else:
            return self._fix_last_letter(word)

    def _fix_last_letter(self, word: str) -> str:
        last_letter = word[-1]
        replacement = self.LAST_LETTERS.get(last_letter, word[-1])
        return word[:-1] + replacement
