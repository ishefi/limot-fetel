#!/usr/bin/env python
from unittest.mock import MagicMock

from lf_base import schemas
from lf_logic.generator_logic import GeneratorLogic
from lf_mocks.lf_test_case import LfTestCase


class TestGeneratorLogic(LfTestCase):
    module_prefix = "lf_logic.generator_logic."

    async def asyncSetUp(self) -> None:
        self.curr_char_index = 0
        self.x_gen_random_root, self.m_gen_random_root = self.xpatch_object(
            GeneratorLogic, "_gen_random_root"
        )
        self.m_gen_random_root.return_value = schemas.Root(p="א", a="ב", l="ג")
        self.m_get_fixers = self.patch_module("get_fixers")
        self.m_get_fixers.return_value = []
        self.templates = ["פועל"]
        self.weights = ["קטול"]
        self.m_milon = self.patch_module("milon")
        self.m_HeEn = self.m_milon.dictionaries.DictionaryHeEn
        self.m_HeEn.return_value.words = []
        self._testee = None

    @property
    def testee(self):
        # to make sure we patch some things before the testee is created
        if self._testee is None:
            self._testee = GeneratorLogic(self.templates, self.weights)
        return self._testee

    async def test_generate(self):
        # act
        result = await self.testee.generate(
            num_of_roots=1, pe=None, ain=None, lamed=None
        )

        # assert
        self.assert_contains_key_value(result, "roots", ["א-ב-ג"])
        self.assert_contains_key_value(result, "templates", self.templates)
        self.assert_contains_key_value(result, "weights", self.weights)
        data = self.assert_contains(result, "data")
        self.assertCountEqual(
            [
                {"populated": "אבוג", "root": "א-ב-ג", "template": "קטול"},
                {"populated": "אובג", "root": "א-ב-ג", "template": "פועל"},
            ],
            data,
        )
        self.m_gen_random_root.assert_called_once_with(None, None, None)
        self.m_HeEn.assert_called_once_with(limit=0)
        self.m_get_fixers.assert_called_once_with()

    async def test_generate_specific_pal(self):
        # arrange
        self.x_gen_random_root.stop()

        # act
        result = await self.testee.generate(num_of_roots=1, pe="ר", ain="ש", lamed="ת")

        # assert
        self.assert_contains_key_value(result, "roots", ["ר-ש-ת"])
        data = self.assert_contains(result, "data")
        self.assertCountEqual(
            [
                {"populated": "רשות", "root": "ר-ש-ת", "template": "קטול"},
                {"populated": "רושת", "root": "ר-ש-ת", "template": "פועל"},
            ],
            data,
        )

    async def test_no_duplicate_roots(self):
        # act
        result = await self.testee.generate(
            num_of_roots=12, pe=None, ain=None, lamed=None
        )

        # assert
        self.assert_contains_key_value(result, "roots", ["א-ב-ג"])
        data = self.assert_contains(result, "data")
        self.assertCountEqual(
            [
                {"populated": "אבוג", "root": "א-ב-ג", "template": "קטול"},
                {"populated": "אובג", "root": "א-ב-ג", "template": "פועל"},
            ],
            data,
        )
        self.assertEqual(12, self.m_gen_random_root.call_count)

    async def test_multiple_roots(self):
        # arrange
        self.x_gen_random_root.stop()
        num_of_roots = 5

        # act
        result = await self.testee.generate(
            num_of_roots=num_of_roots, pe=None, ain=None, lamed=None
        )

        self.assert_len(result["roots"], num_of_roots)
        self.assert_len(
            result["data"], num_of_roots * len(self.templates + self.weights)
        )

    async def test_last_letter_fixing(self):
        # arrange
        self.m_gen_random_root.return_value = schemas.Root(p="מ", a="מ", l="מ")

        # act
        result = await self.testee.generate(
            num_of_roots=1, pe=None, ain=None, lamed=None
        )

        # assert
        data = self.assert_contains(result, "data")
        nonwords = [d["populated"] for d in data]
        self.assertCountEqual(["מומם", "ממום"], nonwords)

    async def test_dictionary_filtering(self):
        # arrange
        self.m_HeEn.return_value.words = [{"translated": "אבוג"}]

        # act
        result = await self.testee.generate(
            num_of_roots=1, pe=None, ain=None, lamed=None
        )

        # assert
        data = self.assert_contains(result, "data")
        self.assertCountEqual(
            [{"populated": "אובג", "root": "א-ב-ג", "template": "פועל"}], data
        )

    async def test_fixtures(self):
        # arrange
        m_fixer = MagicMock()
        self.m_get_fixers.return_value = [m_fixer]
        expected_nons = [
            schemas.NonWord(populated="אבוג", root="א-ב-ג", template="קטול"),
            schemas.NonWord(populated="אובג", root="א-ב-ג", template="פועל"),
        ]

        # act
        result = await self.testee.generate(
            num_of_roots=1, pe=None, ain=None, lamed=None
        )

        # assert
        for expected_non in expected_nons:
            m_fixer.fix.assert_any_call(expected_non)

        data = self.assert_contains(result, "data")
        self.assertCountEqual([non.dict() for non in expected_nons], data)
