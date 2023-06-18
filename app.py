#!/usr/bin/env python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic.main import BaseModel

from lf_logic import consts
from lf_logic.generator_logic import GeneratorLogic

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


jtemplates = Jinja2Templates(directory="templates")


class NonResponse(BaseModel):
    templates: list[str]
    weights: list[str]
    roots: list[str]
    data: list[dict[str, str]]


@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    return jtemplates.TemplateResponse(
        "index.html", {"request": request, "weights": consts.WEIGHTS, "templates": consts.VERB_TEMPLATES}
    )


@app.get("/api/non-words")
async def get_non_words(
        weights: str | None = None,
        templates: str | None = None,
        p: str | None = None,
        a: str | None = None,
        l: str | None = None,
        number_of_roots: int = 5

) -> NonResponse:
    if templates:
        templates = templates.split(",")
    if weights:
        weights = weights.split(",")
    logic = GeneratorLogic(templates=templates, weights=weights)
    return await logic.generate(
        p=p, a=a, l=l, num_of_roots=number_of_roots
    )

