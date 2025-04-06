import numpy as np
from collections import defaultdict

def clean_data(data_points):
    """
    Clean sensor data by:
    1. Removing duplicate entries
    2. Handling missing values through interpolation or nearest neighbors
    3. Smoothing noisy data with moving average
    """
    if not data_points:
        return []
    
    # Remove exact duplicates and convert None values to np.nan
    unique_data = []
    seen = set()
    
    for point in data_points:
        # Convert None to np.nan for easier processing
        clean_point = []
        for value in point:
            if value is None or (isinstance(value, float) and np.isnan(value)):
                clean_point.append(np.nan)
            else:
                clean_point.append(value)
        
        point_tuple = tuple(clean_point)
        if point_tuple not in seen:
            seen.add(point_tuple)
            unique_data.append(clean_point)
    
    # Convert to numpy array for easier processing
    data_array = np.array(unique_data, dtype=float)
    
    # Handle missing values with interpolation if possible, otherwise use nearest neighbors
    for i in range(data_array.shape[1]):
        column = data_array[:, i]
        mask = np.isnan(column)
        
        if np.all(mask):  # All values are NaN
            data_array[:, i] = 0  # Default to 0 if all values are missing
        elif np.any(mask):  # Some values are NaN
            # Get indices of non-NaN values
            valid_indices = np.where(~mask)[0]
            # Get indices of NaN values
            nan_indices = np.where(mask)[0]
            
            if len(valid_indices) > 0:
                # Use nearest neighbor interpolation
                for j in nan_indices:
                    # Find nearest valid index
                    nearest_idx = valid_indices[np.abs(valid_indices - j).argmin()]
                    data_array[j, i] = data_array[nearest_idx, i]
    
    # Simple smoothing with moving average (window=3)
    if len(data_array) > 3:
        window_size = 3
        weights = np.ones(window_size) / window_size
        for i in range(data_array.shape[1]):
            # Use 'valid' mode to avoid edge effects
            smoothed = np.convolve(data_array[:, i], weights, mode='same')
            # Don't modify the edges (first and last elements)
            data_array[1:-1, i] = smoothed[1:-1]
    
    return data_array.tolist()

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
        # Skip NaN values
        valid_mask = ~np.isnan(column)
        valid_data = column[valid_mask]
        
        if len(valid_data) < 2 or np.std(valid_data) == 0:  # not enough data or no variation
            continue
        
        mean = np.mean(valid_data)
        std = np.std(valid_data)
        
        # Calculate z-scores only for non-NaN values
        z_scores = np.zeros_like(column)
        z_scores[valid_mask] = np.abs((valid_data - mean) / std)
        
        # Flag anomalies
        anomalies = anomalies | (z_scores > threshold)
    
    return anomalies.tolist()