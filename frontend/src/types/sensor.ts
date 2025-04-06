export interface SensorData {
  id: number;
  temperature: number | null;
  humidity: number | null;
  air_quality: number | null;
  timestamp: string;
  is_anomaly: boolean;
  is_cleaned: boolean;
}

export interface AggregatedStats {
  time_window: string;
  temperature_mean: number;
  temperature_median: number;
  temperature_min: number;
  temperature_max: number;
  humidity_mean: number;
  humidity_median: number;
  humidity_min: number;
  humidity_max: number;
  air_quality_mean: number;
  air_quality_median: number;
  air_quality_min: number;
  air_quality_max: number;
}