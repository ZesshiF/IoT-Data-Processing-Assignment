from sqlalchemy.orm import Session
from . import models
from datetime import datetime, timedelta
from .utils.data_processing import clean_data, detect_anomalies

def create_sensor_data(db: Session, sensor_data):
    try:
        db_data = models.SensorData(**sensor_data.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
        return db_data
    except Exception as e:
        db.rollback()
        raise e

def get_sensor_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SensorData).offset(skip).limit(limit).all()

def get_aggregated_stats(db: Session, time_window: str = "10m"):
    now = datetime.utcnow()
    
    if time_window == "10m":
        start_time = now - timedelta(minutes=10)
    elif time_window == "1h":
        start_time = now - timedelta(hours=1)
    elif time_window == "24h":
        start_time = now - timedelta(hours=24)
    else:
        start_time = now - timedelta(minutes=10)  # default
    
    data = db.query(models.SensorData).filter(
        models.SensorData.timestamp >= start_time
    ).all()
    
    if not data:
        return None
    
    # Calculate statistics
    temperatures = [d.temperature for d in data]
    humidities = [d.humidity for d in data]
    air_qualities = [d.air_quality for d in data]
    
    def calculate_stats(values):
        if not values:
            return (0.0, 0.0, 0.0, 0.0)
        sorted_values = sorted(values)
        n = len(sorted_values)
        return (
            sum(values) / n,
            sorted_values[n//2] if n % 2 else (sorted_values[n//2-1] + sorted_values[n//2])/2,
            min(values),
            max(values)
        )
    
    temp_mean, temp_median, temp_min, temp_max = calculate_stats(temperatures)
    hum_mean, hum_median, hum_min, hum_max = calculate_stats(humidities)
    air_mean, air_median, air_min, air_max = calculate_stats(air_qualities)
    
    return {
        "time_window": time_window,
        "temperature_mean": temp_mean,
        "temperature_median": temp_median,
        "temperature_min": temp_min,
        "temperature_max": temp_max,
        "humidity_mean": hum_mean,
        "humidity_median": hum_median,
        "humidity_min": hum_min,
        "humidity_max": hum_max,
        "air_quality_mean": air_mean,
        "air_quality_median": air_median,
        "air_quality_min": air_min,
        "air_quality_max": air_max,
    }

def process_sensor_data(db: Session):
    # Get unprocessed data
    unprocessed_data = db.query(models.SensorData).filter(
        models.SensorData.is_cleaned == False
    ).all()
    
    if not unprocessed_data:
        return []
    
    # Clean data
    cleaned_data = clean_data([(d.temperature, d.humidity, d.air_quality) for d in unprocessed_data])
    
    # Detect anomalies
    anomalies = detect_anomalies(cleaned_data)
    
    # Update database
    for i, data in enumerate(unprocessed_data):
        data.temperature = cleaned_data[i][0]
        data.humidity = cleaned_data[i][1]
        data.air_quality = cleaned_data[i][2]
        data.is_anomaly = anomalies[i]
        data.is_cleaned = True
        db.add(data)
    
    db.commit()
    
    # Return processed data
    return db.query(models.SensorData).filter(
        models.SensorData.is_cleaned == True
    ).order_by(models.SensorData.timestamp.desc()).limit(100).all()