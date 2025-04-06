from sqlalchemy import Column, Integer, Float, DateTime, Boolean
from sqlalchemy.sql import func
from datetime import datetime
from .database import Base
from sqlalchemy import Index

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    air_quality = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)  # Added index
    is_anomaly = Column(Boolean, default=False)
    is_cleaned = Column(Boolean, default=False)

# Add composite index for common query patterns
Index('idx_sensor_timestamp_cleaned', SensorData.timestamp, SensorData.is_cleaned)