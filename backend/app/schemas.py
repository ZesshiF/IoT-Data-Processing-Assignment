from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SensorDataCreate(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    air_quality: Optional[float] = None

class SensorDataResponse(BaseModel):
    id: int
    temperature: Optional[float]
    humidity: Optional[float]
    air_quality: Optional[float]
    timestamp: datetime
    is_anomaly: bool
    is_cleaned: bool

    class Config:
        orm_mode = True

class AggregatedStatsResponse(BaseModel):
    time_window: str
    temperature_mean: float
    temperature_median: float
    temperature_min: float
    temperature_max: float
    humidity_mean: float
    humidity_median: float
    humidity_min: float
    humidity_max: float
    air_quality_mean: float
    air_quality_median: float
    air_quality_min: float
    air_quality_max: float