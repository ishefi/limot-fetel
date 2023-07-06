#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from lf_base import schemas
from lf_logic.phonologic_fixers.dagesh_kal_fixer import DageshKalFixer
from lf_mocks.lf_test_case import LfTestCase


class TestDageshKalFixer(LfTestCase):
    async def asyncSetUp(self) -> None:
        self.testee = DageshKalFixer()

    async def test_fix__no_fix(self):
        # arrange
        word = schemas.NonWord(populated="קטל", root="", template="")
        original = word.populated

        # act
        self.testee.fix(word)

        # assert
        self.assertEqual(original, word.populated)

    async def test_fix_word_beginning(self):
        # arrange
        word = schemas.NonWord(populated="פעל", root="", template="")
        original = word.populated

        # act
        self.testee.fix(word)

        # assert
        self.assertNotEqual(original, word.populated)
        self.assertEqual("פּעל", word.populated)

    async def test_dont_fix_after_tnua(self):
        # arrange
        word = schemas.NonWord(populated="לַפל", root="", template="")
        original = word.populated

        # act
        self.testee.fix(word)

        # assert
        self.assertEqual(original, word.populated)

    @pytest.mark.skip("TODO: fix shwa na")
    async def test_fix_after_shwa_na(self):
        # arrange
        word = schemas.NonWord(populated="לְפַעֵל", root="", template="")
        original = word.populated

        # act
        self.testee.fix(word)

        # assert
        self.assertEqual(original, word.populated)

    async def test_fix_after_shwa_nax(self):
        # arrange
        word = schemas.NonWord(populated="מִתְבהל", root="", template="")
        original = word.populated

        # act
        self.testee.fix(word)

        # assert
        self.assertNotEqual(original, word.populated)
        self.assertEqual("מִתְבּהל", word.populated)
