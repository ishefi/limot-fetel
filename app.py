#!/usr/bin/env python
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from lf_logic.generator_logic import GeneratorLogic

app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
async def get_words():
    logic = GeneratorLogic()
    return '\n'.join(await logic.generate())
