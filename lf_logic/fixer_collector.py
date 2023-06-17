#!/usr/in/env python
from pathlib import Path

from lf_logic.niqqud_fixers.base_fixer import BaseFixer


def collect_fixers():
    fixer_dir = Path("lf_logic") / Path("niqqud_fixers")
    py_module = str(fixer_dir).replace("/", ".")
    fixers = []
    for mod in Path.iterdir(fixer_dir):
        _fixers_from_file(fixers, py_module, mod)
    return fixers


def _fixers_from_file(fixers, py_module, mod):
    if mod.suffix != ".py":
        return
    module_path = f"{py_module}.{mod.stem}"
    try:
        pkg = __import__(module_path, globals(), locals(), fromlist=["*"])
        potential_fixers = [getattr(pkg, attr, None) for attr in dir(pkg)]
        for potential in potential_fixers:
            if issubclass(potential, BaseFixer) and potential != BaseFixer:
                fixers.append(potential)
    except Exception as ex:
        pass  # TODO: log