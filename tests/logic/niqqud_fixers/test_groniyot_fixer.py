#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lf_logic.niqqud_fixers.groniyot_fixer import GroniyotFixer
from lf_mocks.lf_test_case import LfTestCase


class TestGroniyotFixer(LfTestCase):
    async def asyncSetUp(self) -> None:
        self.testee = GroniyotFixer()

    async def test_fix__no_fix(self):
        # arrange
        word = "קְּטל"

        # act
        result = self.testee.fix(word)

        # assert
        self.assertEqual(word, result)

    async def test_fix_word__shwa(self):
        # arrange
        word = "פעְל"

        # act
        result = self.testee.fix(word)

        # assert
        self.assertNotEqual(word, result)
        self.assertEqual("פעֲל", result)

    async def test_fix_word__dagash(self):
        # arrange
        word = "פעּל"

        # act
        result = self.testee.fix(word)

        # assert
        self.assertNotEqual(word, result)
        self.assertEqual("פעל", result)

    async def test_fix_word__dagash_and_shwa(self):
        # arrange
        word = "פעְּל"

        # act
        result = self.testee.fix(word)

        # assert
        self.assertNotEqual(word, result)
        self.assertEqual("פעֲל", result)
