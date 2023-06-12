#!/usr/bin/env python
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from lf_logic.generator_logic import GeneratorLogic
from typing import Optional


app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
async def get_words(
        p: Optional[str] = None, a: Optional[str] = None, l: Optional[str] = None, number_of_roots: int = 10
):
    logic = GeneratorLogic()
    return '\n'.join(await logic.generate(p=p, a=a, l=l, num_of_roots=number_of_roots))
