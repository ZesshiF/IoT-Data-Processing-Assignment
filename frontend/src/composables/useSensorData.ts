import { ref } from 'vue'
import type { SensorData, AggregatedStats } from '@/types/sensor'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export function useSensorData() {
  const sensorData = ref<SensorData[]>([])
  const aggregatedStats = ref<AggregatedStats | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchSensorData = async () => {
    try {
      loading.value = true
      const response = await fetch(`${API_URL}/sensor/processed`)
      if (!response.ok) throw new Error('Failed to fetch sensor data')
      sensorData.value = await response.json()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error occurred'
    } finally {
      loading.value = false
    }
  }

  const fetchAggregatedStats = async (timeWindow: string = '10m') => {
    try {
      loading.value = true
      const response = await fetch(`${API_URL}/sensor/aggregated?time_window=${timeWindow}`)
      if (!response.ok) throw new Error('Failed to fetch aggregated stats')
      aggregatedStats.value = await response.json()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error occurred'
    } finally {
      loading.value = false
    }
  }

  const submitSensorData = async (
    data: Omit<SensorData, 'id' | 'timestamp' | 'is_anomaly' | 'is_cleaned'>,
  ) => {
    try {
      loading.value = true
      const response = await fetch(`${API_URL}/sensor/data`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      if (!response.ok) throw new Error('Failed to submit sensor data')
      return await response.json()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error occurred'
      return null
    } finally {
      loading.value = false
    }
  }

  return {
    sensorData,
    aggregatedStats,
    loading,
    error,
    fetchSensorData,
    fetchAggregatedStats,
    submitSensorData,
  }
}
