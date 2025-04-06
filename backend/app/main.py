from fastapi import FastAPI
from .database import engine, Base
from .routers import sensor
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="IoT Data Processing API",
    description="API for processing IoT sensor data with anomaly detection",
    version="1.0.0",
)

async def connect_to_db():
    max_retries = 5
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            # Try to create tables (will fail if DB isn't ready)
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
            return
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                import time
                time.sleep(retry_delay)
            else:
                logger.error("Failed to connect to database after multiple attempts")
                raise

@app.on_event("startup")
async def startup_event():
    await connect_to_db()

app.include_router(sensor.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only! Tighten this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "IoT Data Processing Service"}