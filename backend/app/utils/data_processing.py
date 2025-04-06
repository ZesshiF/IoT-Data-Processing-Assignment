import numpy as np
from collections import defaultdict

def clean_data(data_points):
    """More robust data cleaning with validation"""
    if not data_points:
        return []

    cleaned = []
    for point in data_points:
        try:
            # Ensure all 3 values exist, fill missing with None
            temp = float(point[0]) if len(point) > 0 and point[0] not in [None, ""] else None
            humidity = float(point[1]) if len(point) > 1 and point[1] not in [None, ""] else None
            air_quality = float(point[2]) if len(point) > 2 and point[2] not in [None, ""] else None
            
            # Only keep valid data points
            if all(v is not None for v in [temp, humidity, air_quality]):
                cleaned.append((temp, humidity, air_quality))
            else:
                cleaned.append((None, None, None))  # Add placeholder for invalid data
        except (ValueError, IndexError):
            cleaned.append((None, None, None))  # Add placeholder for invalid data
    
    return cleaned


def detect_anomalies(data_points, threshold=3.0):
    """
    Detect anomalies using Z-score method for each sensor metric
    Returns a list of booleans indicating if each data point is anomalous
    """
    if not data_points or len(data_points[0]) != 3:
        return [False] * len(data_points) if data_points else []
    
    data_array = np.array(data_points, dtype=object)  # Use dtype=object to handle None values
    anomalies = np.zeros(len(data_points), dtype=bool)
    
    for i in range(data_array.shape[1]):
        column = data_array[:, i]
        # Filter out None values
        valid_values = np.array([x for x in column if x is not None], dtype=float)
        
        if len(valid_values) == 0:  # Skip if no valid values
            continue
        
        mean = np.mean(valid_values)
        std = np.std(valid_values)
        
        if std == 0:  # No variation
            continue
        
        # Replace None values with the mean for anomaly detection
        column = np.array([x if x is not None else mean for x in column], dtype=float)
        
        z_scores = np.abs((column - mean) / std)
        anomalies = anomalies | (z_scores > threshold)
    
    return anomalies.tolist()