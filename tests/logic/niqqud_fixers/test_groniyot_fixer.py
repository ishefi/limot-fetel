#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lf_base import schemas
from lf_logic.phonologic_fixers.groniyot_fixer import GroniyotFixer
from lf_mocks.lf_test_case import LfTestCase


class TestGroniyotFixer(LfTestCase):
    async def asyncSetUp(self) -> None:
        self.testee = GroniyotFixer()

    async def test_fix__no_fix(self):
        # arrange
        word = schemas.NonWord(populated="קְּטל", root="", template="")
        original = word.populated

        # act
        self.testee.fix(word)

        # assert
        self.assertEqual(original, word.populated)

    async def test_fix_word__shwa(self):
        # arrange
        word = schemas.NonWord(populated="פעְל", root="", template="")
        original = word.populated

        # act
        self.testee.fix(word)

        # assert
        self.assertNotEqual(original, word.populated)
        self.assertEqual("פעֲל", word.populated)

    async def test_fix_word__dagash(self):
        # arrange
        word = schemas.NonWord(populated="פעּל", root="", template="")
        original = word.populated

        # act
        self.testee.fix(word)

        # assert
        self.assertNotEqual(original, word.populated)
        self.assertEqual("פעל", word.populated)

    async def test_fix_word__dagash_and_shwa(self):
        # arrange
        word = schemas.NonWord(populated="פעְּל", root="", template="")
        original = word.populated

        # act
        self.testee.fix(word)

        # assert
        self.assertNotEqual(original, word.populated)
        self.assertEqual("פעֲל", word.populated)
