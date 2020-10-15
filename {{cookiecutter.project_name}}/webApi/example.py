import json
import os
import time

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from typing import Optional, List, Dict

from fastapi import FastAPI, Request, HTTPException, Path, Query
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder

from .configuration.version import __version__
from .controllers.errors import ErrorHandler

from .models.examples import ExampleObject, tags_metadata, BaseModel

from starlette_prometheus import metrics, PrometheusMiddleware



app = FastAPI(openapi_tags=tags_metadata, version=__version__)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)



class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: Optional[str] = None,
    item: Optional[Item] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

@app.get("/items/")
def read_items(
    q: Optional[str] = Query(
        None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/request", tags=["exampleTag"])
def exampleRequest(request: ExampleObject):
    # from package_name.configuration.settings
    # logger = settings.get_logger(__name__)

    try: 
        attribute = request.attribute
        optinalAttribute = request.optinalAttribute
        complexAttribute: request.complexAttribute
        dateAttribute: request.dateAttribute
        customField : request.customField
    except Exception as ex:
        raise HTTPException(detail=f'Error while parsing request: {ex}', status_code=400) 



class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )




# Register error handling so we can manage easily functional errors
@app.exception_handler(ErrorHandler)
def handle_invalid_usage(request: Request, error: ErrorHandler):
  response = JSONResponse(error.to_dict())
  response.status_code = error.status_code
  return response
