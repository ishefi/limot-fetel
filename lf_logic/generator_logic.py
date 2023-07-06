#!/usr/in/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import random
import re

import milon.dictionaries

from lf_logic import consts
from lf_logic.fixer_collector import get_fixers
from lf_base import schemas


class GeneratorLogic:
    CHARS = "אבגדהוזחטיכלמנסעפצקרשת"
    LAST_LETTERS = {
        "מ": "ם",
        "נ": "ן",
        "צ": "ץ",
        "פ": "ף",
        "כ": "ך",
    }

    def __init__(self, templates, weights):
        self.milon = milon.dictionaries.DictionaryHeEn(limit=0)
        self.milon_words = [word["translated"] for word in self.milon.words]
        self.templates = templates or consts.VERB_TEMPLATES
        self.weights = weights or consts.WEIGHTS
        self.fixers = get_fixers()

    async def generate(
        self, num_of_roots: int, pe: str | None, ain: str | None, lamed: str | None
    ):
        roots = set(
            [self._gen_random_root(pe, ain, lamed) for _ in range(num_of_roots)]
        )

        potential_nons: list[schemas.NonWord] = []

        for root in roots:
            potential_nons += [
                self._populate_template(schemas.Template.noun_template(weight), root)
                for weight in self.weights
            ]
            potential_nons += [
                self._populate_template(schemas.Template.verb_template(template), root)
                for template in self.templates
            ]
        return {
            "data": [
                potential.dict()
                for potential in potential_nons
                if self._is_nonword(potential.populated)
            ],
            "roots": [str(root) for root in roots],
            "templates": self.templates,
            "weights": self.weights,
        }

    def _populate_template(self, template: schemas.Template, root: schemas.Root):
        replacer_dict = {
            template.root.p: root.p,
            template.root.a: root.a,
            template.root.l: root.l,
        }

        def replacer(match):
            return replacer_dict[match.string[match.start() : match.end()]]

        populated = re.sub(template.root_regex, replacer, template.template)
        populated = self._fix_last_letter(populated)
        for fixer in self.fixers:
            populated = fixer.fix(populated)
        return schemas.NonWord(
            populated=populated, template=str(template), root=str(root)
        )

    def _gen_random_root(self, pe, ain, lamed) -> schemas.Root:
        return schemas.Root(
            p=pe or random.choice(self.CHARS),
            a=ain or random.choice(self.CHARS),
            l=lamed or random.choice(self.CHARS),
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
