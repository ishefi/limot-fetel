#!/usr/bin/env python
import pprint
import unittest
import unittest.mock


def pp(obj):
    """Format anything nicely."""
    return pprint.PrettyPrinter().pformat(obj)


class LfTestCase(unittest.IsolatedAsyncioTestCase):
    module_prefix = ""

    def patch_module(self, name: str, *args, **kwargs):
        _, mocker = self.xpatch_module(name, *args, **kwargs)
        return mocker

    def xpatch_module(self, name: str, *args, **kwargs):
        if self.module_prefix == "":
            self.fail("Set module_prefix before calling patch_module()")
        return self.xpatch(self.module_prefix + name, *args, **kwargs)

    def patch(self, name, *args, **kwargs):
        _, mocker = self.xpatch(name, *args, **kwargs)
        return mocker

    def xpatch(self, name, *args, **kwargs):
        self._fix_autospec(args, kwargs)
        patcher = unittest.mock.patch(name, *args, **kwargs)
        mocker = patcher.start()
        self.addCleanup(self.stop_patcher, patcher)
        return patcher, mocker

    def patch_object(self, target, attribute, *args, **kwargs):
        _, mocker = self.xpatch_object(target, attribute, *args, **kwargs)
        return mocker

    def xpatch_object(self, target, attribute, *args, **kwargs):
        patcher = unittest.mock.patch.object(target, attribute, *args, **kwargs)
        mocker = patcher.start()
        self.addCleanup(self.stop_patcher, patcher)
        return patcher, mocker

    def stop_patcher(self, patcher):
        try:
            patcher.stop()
        except RuntimeError:
            pass

    def _fix_autospec(self, args, kwargs):
        if not args:
            if "autospec" not in kwargs:
                if "spec" not in kwargs:
                    kwargs["autospec"] = True

    def assert_contains(self, haystack, needle):
        self.assertIsNotNone(haystack)
        self.assertIn(needle, haystack)
        if isinstance(haystack, dict):
            return haystack[needle]

    def assert_contains_key_value(self, haystack, key, value):
        self.assertIsNotNone(haystack)
        actual = self.assert_contains(haystack, key)
        self.assertEqual(
            value,
            actual,
            msg=f'Expected dict["{key}"] to be {pp(value)}, got {pp(actual)}. Dict is: {pp(haystack)}',
        )

    def assert_len(self, obj, expected_len):
        try:
            actual_len = len(obj)
        except TypeError as e:
            self.fail(e)
        self.assertEqual(expected_len, actual_len)
