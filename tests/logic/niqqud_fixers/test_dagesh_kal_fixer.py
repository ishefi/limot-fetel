#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from lf_logic.niqqud_fixers.dagesh_kal_fixer import DageshKalFixer
from lf_mocks.lf_test_case import LfTestCase


class TestDageshKalFixer(LfTestCase):
    async def asyncSetUp(self) -> None:
        self.testee = DageshKalFixer()

    async def test_fix__no_fix(self):
        # arrange
        word = "קטל"

        # act
        result = self.testee.fix(word)

        # assert
        self.assertEqual(word, result)

    async def test_fix_word_beginning(self):
        # arrange
        word = "פעל"

        # act
        result = self.testee.fix(word)

        # assert
        self.assertNotEqual(word, result)
        self.assertEqual("פּעל", result)

    async def test_dont_fix_after_tnua(self):
        # arrange
        word = "לַפל"

        # act
        result = self.testee.fix(word)

        # assert
        self.assertEqual(result, word)

    @pytest.mark.skip("TODO: fix shwa na")
    async def test_fix_after_shwa_na(self):
        # arrange
        word = "לְפַעֵל"

        # act
        result = self.testee.fix(word)

        # assert
        self.assertEqual(result, word)

    async def test_fix_after_shwa_nax(self):
        # arrange
        word = "מִתְבהל"

        # act
        result = self.testee.fix(word)

        # assert
        self.assertNotEqual(word, result)
        self.assertEqual("מִתְבּהל", result)
