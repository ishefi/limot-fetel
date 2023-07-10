#!/usr/in/env python
from __future__ import annotations
import abc
from typing import Protocol

from hebrew import Hebrew

from lf_base import schemas


class Fixer(Protocol):
    ORDER: int

    @staticmethod
    def fix(word: schemas.NonWord) -> None:
        ...  # pragma: no cover


class BaseFixer(abc.ABC):
    DAGESH = "ּ"
    SHEVA = "ְ"

    @staticmethod
    @abc.abstractmethod
    def fix(word: schemas.NonWord) -> None:
        raise NotImplementedError  # pragma: no cover

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
