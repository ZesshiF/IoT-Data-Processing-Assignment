from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from .. import schemas, services
from ..database import get_db

router = APIRouter(prefix="/sensor", tags=["sensor"])

@router.post("/data", response_model=schemas.SensorDataResponse)
def ingest_sensor_data(data: schemas.SensorDataCreate, db: Session = Depends(get_db)):
    return services.create_sensor_data(db, data)

@router.get("/processed", response_model=List[schemas.SensorDataResponse])
def get_processed_data(db: Session = Depends(get_db)):
    return services.process_sensor_data(db)

@router.get("/aggregated", response_model=schemas.AggregatedStatsResponse)
def get_aggregated_stats(time_window: str = "10m", db: Session = Depends(get_db)):
    stats = services.get_aggregated_stats(db, time_window)
    if not stats:
        raise HTTPException(status_code=404, detail="No data available for the selected time window")
    return stats