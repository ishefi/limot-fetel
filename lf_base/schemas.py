#!/usr/in/env python
from pydantic import BaseModel


class Root(BaseModel):
    p: str
    a: str
    l: str

    def __str__(self):
        return f"{self.p}-{self.a}-{self.l}"

    def __hash__(self):
        return hash((type(self), self.p, self.a, self.l))


class Template(BaseModel):
    root: Root
    template: str

    def __str__(self):
        return self.template

    @staticmethod
    def noun_template(template):
        return Template(root=Root(p="ק", a="ט", l="ל"), template=template)

    @staticmethod
    def verb_template(template):
        return Template(root=Root(p="פ", a="ע", l="ל"), template=template)

    @property
    def root_regex(self):
        return f"({self.root.p})|({self.root.a})|({self.root.l})"


class NonWord(BaseModel):
    populated: str
    template: str
    root: str
