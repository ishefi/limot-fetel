#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from collections import defaultdict
import random
import re

import milon.dictionaries
from pydantic import BaseModel

from lf_logic import consts


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
            templated_root = [
                self._populate_template(Template.noun_template(weight), root)
                for weight in self.weights
            ]
            potential_nons += random.choices(templated_root, k=min(len(templated_root), 10))
            potential_nons += [
                self._populate_template(Template.verb_template(template), root)
                for template in self.templates
            ]
        potential_nons = set(potential_nons)

        nons = defaultdict(list)
        for potential, template in potential_nons:
            if self._is_nonword(potential):
                nons[template].append(potential)
        return [{"template": template, "nons": nons} for template, nons in nons.items()]

    def _populate_template(self, template: Template, root: Root):
        replacer_dict = {
            template.root.p: root.p, template.root.a: root.a, template.root.l: root.l
        }
        replacer = lambda match: replacer_dict[match.string[match.start(): match.end()]]
        populated = re.sub(template.root_regex, replacer, template.template)
        return self._fix_last_letter(populated), template.template

    def _gen_random_root(self, p, a, l) -> Root:
        return Root(
            p=p or random.choice(self.CHARS),
            a=a or random.choice(self.CHARS),
            l=l or random.choice(self.CHARS),
        )

    def _is_nonword(self, word: str) -> bool:
        if word in self.milon_words:
            return False
        else:
            return True

    def _fix_last_letter(self, word: str) -> str:
        last_letter = word[-1]
        replacement = self.LAST_LETTERS.get(last_letter, word[-1])
        return word[:-1] + replacement
