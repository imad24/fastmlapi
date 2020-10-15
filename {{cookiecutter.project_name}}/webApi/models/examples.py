from typing import Optional, List, Dict
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime, time, timedelta
from enum import Enum



tags_metadata = [
    {
        "name": "Forecast Request",
        "description": "Forecast body request that must be sent to demandsensing API",
    }
]



class ForecastRequestModel(BaseModel):
	model : str
	horizonDate : datetime
	hyperParams : Dict
	values : List[str]
	dateStart : datetime
	dateEnd : datetime
	dateFormat : Optional[str]
	chrono : str
	confidenceInterval : Optional[float] = Field(
        0,
        title="Confidence Interval",
        description="Percentage of confidence interval to be taken into account when calculating the forecast",
        ge=0,
        lt=1
    )
	externalVariables : Optional[List[List]] = None
	firstDayOfWeek : Optional[str] = "Monday"
	metrics : List[str]
	seasonality : Optional[List[str]]


#example of Enum use
class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING ="WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ExampleObject(BaseModel):
    id: UUID
    attribute: str
    optinalAttribute: Optional[int]
    complexAttribute: Optional[List[Dict]]
    dateAttribute: datetime
    customField : int = Field(
        5,
        title="",
        description="",
        gt = 3,
        example=55
    )
