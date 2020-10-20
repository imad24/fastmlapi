import json
import os
import time

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from fastapi import FastAPI, HTTPException, Path, Query, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from starlette_prometheus import PrometheusMiddleware, metrics

from .configuration.version import __version__
from .controllers.exceptions import InnerException
from .models.examples import ExampleObject, tags_metadata

app = FastAPI(openapi_tags=tags_metadata, version=__version__)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)

#provides server status information
@app.get('/health', tags=["serverStatus"])
def serverStatus():
  import logging
  from psutil import cpu_percent, virtual_memory
  from .configuration.version import __version__

  try:
    status = {
          "status": "UP",
          "package_version" : __version__,
          "log_level": os.getenv("LOG_LEVEL", logging.getLevelName(logging.INFO)),
          "health":None,
          "cpu_percent": cpu_percent(),
          "memory_precent": virtual_memory().percent,
          "calls_count": None,
          "fails_count": None}
    return status
  except Exception as exc:
     raise HTTPException(status_code=400, detail=str(exc))