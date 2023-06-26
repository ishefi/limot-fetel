#!/usr/in/env python
import abc
from typing import Protocol

from hebrew import Hebrew


class Fixer(Protocol):
    @staticmethod
    def fix(word: str) -> str:
        ...


class BaseFixer(abc.ABC):
    DAGESH = "ּ"
    SHEVA = "ְ"

    @staticmethod
    def fix(word: str) -> str:
        raise NotImplementedError

    @staticmethod
    def _get_graphemes(word: str) -> list[str]:
        hebrew_word = Hebrew(word)
        return [str(g) for g in hebrew_word.graphemes]

    @staticmethod
    def _has_dagesh(grapheme: str) -> bool:
        return BaseFixer.DAGESH in grapheme

    @staticmethod
    def _has_sheva(grapheme: str) -> bool:
        return BaseFixer.SHEVA in grapheme
