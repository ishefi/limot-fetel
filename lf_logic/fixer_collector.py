#!/usr/in/env python
import inspect

from pathlib import Path

from lf_logic.niqqud_fixers.base_fixer import BaseFixer
from lf_logic.niqqud_fixers.base_fixer import Fixer

_FIXERS: list[Fixer] | None = None


def get_fixers() -> list[Fixer]:
    global _FIXERS
    if _FIXERS is None:
        _FIXERS = collect_fixers()
    return _FIXERS


def collect_fixers() -> list[Fixer]:
    fixer_dir = Path("lf_logic") / Path("niqqud_fixers")
    py_module = str(fixer_dir).replace("/", ".")
    fixers: list[Fixer] = []
    for mod in Path.iterdir(fixer_dir):
        _fixers_from_file(fixers, py_module, mod)
    return fixers


def _fixers_from_file(fixers, py_module, mod) -> None:
    if mod.suffix != ".py":
        return
    module_path = f"{py_module}.{mod.stem}"
    try:
        module = __import__(module_path, globals(), locals(), fromlist=["*"])
        potential_fixers = [getattr(module, attr, None) for attr in dir(module)]
        for name, klass in inspect.getmembers(module, inspect.isclass):
            is_defined_in_module = inspect.getmodule(klass) == module
            is_fixer = issubclass(klass, BaseFixer)
            is_concrete = not inspect.isabstract(klass)
            if is_defined_in_module and is_fixer and is_concrete:
                fixers.append(klass())
    except Exception:
        pass  # TODO: log
