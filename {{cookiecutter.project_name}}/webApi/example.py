import json
import os
import time

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from typing import Optional, List, Dict

from fastapi import FastAPI, Request, HTTPException, Path, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder

from .configuration.version import __version__
from .controllers.exceptions import InnerException

from .models.examples import ExampleObject, ForecastRequestModel, tags_metadata, BaseModel

from starlette_prometheus import metrics, PrometheusMiddleware



app = FastAPI(openapi_tags=tags_metadata, version=__version__)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)






@app.post('/forecast/'
        ,tags=["Forecasts"]
        ,summary="Calculates the forecast of a given series"
        ,response_description="The calculated forecast"
        ,response_model=ForecastRequestModel)
def forecast(forecastRequestModel: ForecastRequestModel):
    """Calculates the forecast from the series in the body of the request
    """
    return forecastRequestModel
    


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.put("/items/{item_id}", tags=["Examples"])
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

@app.get("/items/", tags=["Examples"])
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


def train():
    try:
        # do some work here and then something happens
        raise ValueError("The requested model ID couldn't be found !")
    except Exception as exc:
        raise InnerException(error="Could not load model", message=str(exc), loc=__name__)

@app.get("/items/{item_id}", tags=["Examples"],
summary="Example of exception handling")
async def read_item(item_id: int):
    try:    
        train()
    except InnerException as innerExc:
        raise HTTPException(status_code=500, detail=innerExc.json())
    return {"item_id": item_id}



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/request", tags=["Examples"])
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