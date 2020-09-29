from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


tags_metadata = [
    {
        "name": "exampleTag",
        "description": "Used as an example of tag using in docs",
    },
    {
        "name" : "serverStatus",
        "description" : "Gives Status and Health information about the running server"
    }
]

#example of Enum use
class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING ="WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ExampleObject(BaseModel):
    attribute: str
    optinalAttribute: Optional[int]
    complexAttribute: Optional[List[Dict]]
    dateAttribute: datetime
    customField : int = Field(
        5,
        title="",
        description="",
        gt = 3
    )


class ServerStatus(BaseModel):
    Status: str
    PackageVersion : str
    LogLevel: LogLevel
    Health: Optional[str] = None
    CallsCount: Optional[int] = None
    FailsCount: Optional[int] = None
