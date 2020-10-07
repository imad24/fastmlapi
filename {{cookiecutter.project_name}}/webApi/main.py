import json
import os
import time

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


from fastapi import FastAPI, Request, HTTPException, Path, Query
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder

from configuration.version import __version__
from controllers.ErrorHandler import ErrorHandler

from models.examples import ExampleObject, tags_metadata

from starlette_prometheus import metrics, PrometheusMiddleware



app = FastAPI(openapi_tags=tags_metadata, version=__version__)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


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



#provides server status information
@app.get('/status', tags=["serverStatus"])
def serverStatus():
#   from package_name.version import __version__
#   from package_name.configuration.settings import logging_level
  from models.examples import ServerStatus, LogLevel
  __version__, logging_level = "1.0.0", LogLevel.INFO
  
  try:
    status = ServerStatus(**{
          "Status": "The server is UP",
          "PackageVersion" : __version__,
          "LogLevel": logging_level,
          "Health":None,
          "CallsCount": None,
          "FailsCount": None})
    return status
  except Exception as exc:
     raise HTTPException(status_code=400, detail=str(exc))

# Register error handling so we can manage easily functional errors
@app.exception_handler(ErrorHandler)
def handle_invalid_usage(request: Request, error: ErrorHandler):
  response = JSONResponse(error.to_dict())
  response.status_code = error.status_code
  return response
