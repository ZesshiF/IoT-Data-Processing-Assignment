import numpy as np
from collections import defaultdict

def clean_data(data_points):
    """
    Clean sensor data by:
    1. Removing duplicate entries
    2. Handling missing values by interpolation
    3. Smoothing noisy data with moving average
    """
    if not data_points:
        return []
    
    # Remove exact duplicates
    unique_data = []
    seen = set()
    
    for point in data_points:
        point_tuple = tuple(point)
        if point_tuple not in seen:
            seen.add(point_tuple)
            unique_data.append(point)
    
    # Convert to numpy array for easier processing
    data_array = np.array(unique_data)
    
    # Handle missing values (NaN) by forward filling
    mask = np.isnan(data_array)
    idx = np.where(~mask, np.arange(mask.shape[0])[:, None], 0)
    np.maximum.accumulate(idx, axis=0, out=idx)
    cleaned_data = data_array[idx[np.arange(idx.shape[0])[:, None], np.arange(idx.shape[1])]]
    
    # Simple smoothing with moving average (window=3)
    window_size = 3
    if len(cleaned_data) > window_size:
        weights = np.ones(window_size) / window_size
        for i in range(cleaned_data.shape[1]):
            cleaned_data[:, i] = np.convolve(cleaned_data[:, i], weights, mode='same')
    
    return cleaned_data.tolist()

def detect_anomalies(data_points, threshold=3.0):
    """
    Detect anomalies using Z-score method for each sensor metric
    Returns a list of booleans indicating if each data point is anomalous
    """
    if not data_points or len(data_points) < 2:
        return [False] * len(data_points)
    
    data_array = np.array(data_points)
    anomalies = np.zeros(len(data_points), dtype=bool)
    
    for i in range(data_array.shape[1]):
        column = data_array[:, i]
        mean = np.mean(column)
        std = np.std(column)
        
        if std == 0:  # no variation
            continue
            
        z_scores = np.abs((column - mean) / std)
        anomalies = anomalies | (z_scores > threshold)
    
    return anomalies.tolist()