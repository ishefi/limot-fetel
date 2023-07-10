#!/usr/bin/env python
import os
import random
import tempfile

from lf_mocks.lf_test_case import LfTestCase
from lf_logic import fixer_collector


class TestFixerCollector(LfTestCase):
    async def asyncSetUp(self) -> None:
        self.m_iterdir = self.patch_object(fixer_collector.Path, "iterdir")
        self.m_iterdir.return_value = []
        self.fixers_path = (
            fixer_collector.Path(fixer_collector.__file__).parent / "phonologic_fixers"
        )
        self._fixer_import = (
            "from lf_logic.phonologic_fixers.base_fixer import BaseFixer"
        )
        self._mock_fixer_template = (
            self._fixer_import + "\n"
            "class MockFixer(BaseFixer):\n"
            "    ORDER = {order}\n"
            "    def fix(word): pass"
        )

    def mk_temp_mocker(self, filedir=None, suffix=".py", content=None):
        if filedir is None:
            filedir = self.fixers_path
        if content is None:
            content = self._mock_fixer_template.format(order=1)
        temp = self.mk_temp_file(filedir, suffix, content)
        temp_mod = fixer_collector.Path(temp.name)
        self.m_iterdir.return_value = [temp_mod]
        return temp_mod

    def mk_temp_file(self, filedir, suffix, content):
        temp = tempfile.NamedTemporaryFile(
            mode="w", delete=False, prefix="temp-", dir=filedir, suffix=suffix
        )
        with temp as f:
            f.write(content)
        self.addCleanup(lambda: os.remove(temp.name))
        return temp

    def test_collect_fixers__no_fixers(self):
        # act
        fixers = fixer_collector.collect_fixers()

        # assert
        self.m_iterdir.assert_called_once_with(self.fixers_path)
        self.assertEqual([], fixers)

    def test_collect_fixers__collect_some_fixer(self):
        # arrange
        temp_mod = self.mk_temp_mocker()

        # act
        fixers = fixer_collector.collect_fixers()

        # assert
        (fixer,) = fixers
        self.assertEqual(
            str(fixer.__class__),
            f"<class 'lf_logic.phonologic_fixers.{temp_mod.stem}.MockFixer'>",
        )

    def test_collect_fixers__collect_only_py_files(self):
        # arrange
        self.mk_temp_mocker(suffix=".pyc")

        # act
        fixers = fixer_collector.collect_fixers()

        # assert
        self.assertEqual([], fixers)

    def test_collect_only_base_fixer_subclasses(self):
        # arrange
        content = (
            self._fixer_import + "\n" "class MockFixer: \n" "    def fix(word): pass"
        )
        self.mk_temp_mocker(content=content)

        # act
        fixers = fixer_collector.collect_fixers()

        # assert
        self.assertEqual([], fixers)

    def test_collect_only_concrete(self):
        # arrange
        content = self._mock_fixer_template.format(order=1).replace(" fix(", " fux(")
        self.mk_temp_mocker(content=content)

        # act
        fixers = fixer_collector.collect_fixers()

        # assert
        self.assertEqual([], fixers)

    def test_dont_collect_things_that_were_imported(self):
        # arrange
        another_dir = self.fixers_path.parent
        another_mocker = self.mk_temp_mocker(filedir=another_dir)
        content = f"from lf_logic.{another_mocker.stem} import MockFixer"
        self.mk_temp_mocker(content=content)

        # act
        fixers = fixer_collector.collect_fixers()

        # assert
        self.assertEqual([], fixers)

    def test_dont_care_for_exceptions(self):
        # arrange
        mods = [self.mk_temp_mocker() for _ in range(20)]
        mods.append(self.mk_temp_mocker(content="BAD FILE!"))
        random.shuffle(mods)  # make sure the bad file is not the last one
        self.m_iterdir.return_value = mods

        # act
        fixers = fixer_collector.collect_fixers()

        # assert
        self.assert_len(fixers, 20)

    def test_collect_fixers_once(self):
        # arrange
        fixers_before = fixer_collector.get_fixers()
        self.mk_temp_mocker()

        # act
        fixers_after = fixer_collector.get_fixers()

        # assert
        self.assertEqual(fixers_before, fixers_after)

    def test_collect_fixer_by_order(self):
        # arrange
        orders = [1, 42, 50]
        mods = [
            self.mk_temp_mocker(content=self._mock_fixer_template.format(order=order))
            for order in orders
        ]
        random.shuffle(mods)
        self.m_iterdir.return_value = mods

        # act
        fixers = fixer_collector.collect_fixers()

        # assert
        self.assertListEqual(orders, [fixer.ORDER for fixer in fixers])
