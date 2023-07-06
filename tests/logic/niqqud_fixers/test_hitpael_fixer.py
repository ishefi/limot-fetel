#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lf_base import schemas
from lf_logic.phonologic_fixers.hitpael_fixer import HitpaelFixer
from lf_mocks.lf_test_case import LfTestCase


class TestHitpaelFixer(LfTestCase):
    async def asyncSetUp(self) -> None:
        self.hitpael_template = "הִתְפַעֵּל"
        self.testee = HitpaelFixer()

    async def test_fix_hitpael_metathesis(self):
        # arrange
        word = schemas.NonWord(
            populated="הִתְסַעֵל", root="ס-ע-ל", template=self.hitpael_template
        )

        # act
        self.testee.fix(word)

        # assert
        self.assertEqual("הִסְתַעֵל", word.populated)

    async def test_dont_fix_if_not_hitpael(self):
        # arrange
        word = schemas.NonWord(
            populated="הִתְסַעֵל", root="ס-ע-ל", template="some other template"
        )
        original = word.populated

        # act
        self.testee.fix(word)

        # assert
        self.assertEqual(original, word.populated)

    async def test_dont_fix_if_not_sibilant(self):
        # arrange
        word = schemas.NonWord(
            populated="הִתְפַעֵל", root="פ-ע-ל", template=self.hitpael_template
        )
        original = word.populated

        # act
        self.testee.fix(word)

        # assert
        self.assertEqual(original, word.populated)

    async def test_fix_hitpael__metathesis_and_voice_assimilation(self):
        # arrange
        word = schemas.NonWord(
            populated="הִתְזַעֵל", root="ז-ע-ל", template=self.hitpael_template
        )

        # act
        self.testee.fix(word)

        # assert
        self.assertEqual("הִזְדַעֵל", word.populated)

    async def test_fix_hitpael__metathesis_and_emphatic_assimilation(self):
        # arrange
        word = schemas.NonWord(
            populated="הִתְצַעֵל", root="צ-ע-ל", template=self.hitpael_template
        )

        # act
        self.testee.fix(word)

        # assert
        self.assertEqual("הִצְטַעֵל", word.populated)
