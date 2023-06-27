#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fastapi.testclient

from app import NonResponse
from app import app
from lf_mocks.lf_test_case import LfTestCase


class TestApp(LfTestCase):
    module_prefix = "app."

    async def asyncSetUp(self) -> None:
        self.client = fastapi.testclient.TestClient(app)
        self.x_GeneratorLogic, self.m_GeneratorLogic = self.xpatch_module(
            "GeneratorLogic"
        )
        self.m_generator_logic = self.m_GeneratorLogic.return_value
        self.m_generator_logic.generate.return_value = NonResponse(
            templates=[], weights=[], roots=[], data=[]
        )

    async def test_get_index(self):
        # act
        response = self.client.get("/")

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertIn("פָעַל", response.text)
        self.assertIn("קִטֵּל", response.text)

    async def test_get_non_words(self):
        # act
        response = self.client.get("/api/non-words")

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {"templates": [], "weights": [], "roots": [], "data": []},
            response.json(),
        )
        self.m_GeneratorLogic.assert_called_once_with(templates=[], weights=[])
        self.m_generator_logic.generate.assert_called_once_with(
            pe=None, ain=None, lamed=None, num_of_roots=5
        )

    async def test_get_non_words__with_params(self):
        # act
        response = self.client.get(
            "/api/non-words",
            params="weights=a,b,c&templates=1,2,3&p=p&a=a&l=l&number_of_roots=4",
        )

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {"templates": [], "weights": [], "roots": [], "data": []},
            response.json(),
        )
        self.m_GeneratorLogic.assert_called_once_with(
            templates=["1", "2", "3"], weights=["a", "b", "c"]
        )
        self.m_generator_logic.generate.assert_called_once_with(
            pe="p", ain="a", lamed="l", num_of_roots=4
        )

    async def test_get_non_words_e2e(self):
        # arrange
        self.x_GeneratorLogic.stop()

        # act
        response = self.client.get(
            "/api/non-words",
            params="weights=קוטל&templates=פעול&p=נ&a=ש&l=כ&number_of_roots=1",
        )

        # assert
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assert_contains_key_value(response_json, "roots", ["נ-ש-כ"])
        self.assert_contains_key_value(response_json, "templates", ["פעול"])
        self.assert_contains_key_value(response_json, "weights", ["קוטל"])
        words = self.assert_contains(response_json, "data")
        self.assertCountEqual(
            [
                {"populated": "נושך", "template": "קוטל", "root": "נ-ש-כ"},
                {"populated": "נשוך", "template": "פעול", "root": "נ-ש-כ"},
            ],
            words,
        )
