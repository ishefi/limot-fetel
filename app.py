#!/usr/bin/env python
from fastapi import FastAPI
from fastapi import Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from lf_logic import consts
from lf_logic.generator_logic import GeneratorLogic

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


jtemplates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    return jtemplates.TemplateResponse(
        "index.html", {"request": request, "weights": consts.WEIGHTS, "templates": consts.VERB_TEMPLATES}
    )


@app.get("/api/non-words")
async def get_non_words(
        weights: list[str] | None = Query(None),
        templates: list[str] | None = Query(None),
        p: str | None = None,
        a: str | None = None,
        l: str | None = None,
        number_of_roots: int = 10

):
    if weights == [""]:
        weights = None
    if templates == [""]:
        templates = None
    logic = GeneratorLogic(templates=templates, weights=weights)
    return await logic.generate(
        p=p, a=a, l=l, num_of_roots=number_of_roots
    )
