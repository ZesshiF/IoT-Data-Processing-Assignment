
CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    temperature FLOAT,
    humidity FLOAT,
    air_quality FLOAT,
    is_anomaly BOOLEAN DEFAULT FALSE,
    is_cleaned BOOLEAN DEFAULT FALSE
);

COPY sensor_data(timestamp, temperature, humidity, air_quality) 
FROM '/docker-entrypoint-initdb.d/sensor_data.csv' DELIMITER ',' CSV HEADER;