#!/usr/in/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import random
import re

import milon.dictionaries
from pydantic import BaseModel

from lf_logic import consts
from lf_logic.fixer_collector import collect_fixers

FIXERS = collect_fixers()


class Root(BaseModel):
    p: str
    a: str
    l: str

    def __str__(self):
        return f'{self.p}-{self.a}-{self.l}'

    def __hash__(self):
        return hash((type(self), self.p, self.a, self.l))


class Template(BaseModel):
    root: Root
    template: str

    def __str__(self):
        return self.template

    @staticmethod
    def noun_template(template):
        return Template(root=Root(p='ק', a='ט', l='ל'), template=template)

    @staticmethod
    def verb_template(template):
        return Template(root=Root(p='פ', a='ע', l='ל'), template=template)

    @property
    def root_regex(self):
        return f'({self.root.p})|({self.root.a})|({self.root.l})'


class NonWord(BaseModel):
    populated: str
    template: str
    root: str

    def __eq__(self, other):
        return self.populated == other.populated

    def __hash__(self):
        return hash((type(self), self.populated))


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

    async def generate(
            self, num_of_roots: int, p: str | None, a: str | None, l: str | None
    ):
        roots = set([self._gen_random_root(p, a, l) for _ in range(num_of_roots)])

        potential_nons: list[NonWord] = []

        for root in roots:
            potential_nons += [
                self._populate_template(Template.noun_template(weight), root)
                for weight in self.weights
            ]
            potential_nons += [
                self._populate_template(Template.verb_template(template), root)
                for template in self.templates
            ]
        return {
            "data": [
                potential.dict() for potential in set(potential_nons)
                if self._is_nonword(potential.populated)
            ],
            "roots": [str(root) for root in roots],
            "templates": self.templates,
            "weights": self.weights,
        }

    def _populate_template(self, template: Template, root: Root):
        replacer_dict = {
            template.root.p: root.p, template.root.a: root.a, template.root.l: root.l
        }
        replacer = lambda match: replacer_dict[match.string[match.start(): match.end()]]
        populated = re.sub(template.root_regex, replacer, template.template)
        populated = self._fix_last_letter(populated)
        for Fixer in FIXERS:
            fixer = Fixer()
            populated = fixer.fix(populated)
        return NonWord(populated=populated, template=str(template), root=str(root))

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
