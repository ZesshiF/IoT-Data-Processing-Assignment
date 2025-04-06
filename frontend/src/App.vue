<script setup lang="ts">
import { ref, onMounted } from 'vue'
import SensorChart from './components/SensorChart.vue'
import SensorStats from './components/SensorStats.vue'
import { useSensorData } from './composables/useSensorData'

const { sensorData, aggregatedStats, loading, error, fetchSensorData, fetchAggregatedStats } =
  useSensorData()

const timeWindow = ref('10m')
const newData = ref({
  temperature: 0,
  humidity: 0,
  air_quality: 0,
})

onMounted(() => {
  fetchSensorData()
  fetchAggregatedStats(timeWindow.value)
})

const handleTimeWindowChange = (window: string) => {
  timeWindow.value = window
  fetchAggregatedStats(window)
}

const submitData = async () => {
  await useSensorData().submitSensorData(newData.value)
  fetchSensorData()
  fetchAggregatedStats(timeWindow.value)
  newData.value = { temperature: 0, humidity: 0, air_quality: 0 }
}
</script>

<template>
  <div class="app-container">
    <h1>IoT Sensor Data Dashboard</h1>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div class="data-input">
      <h3>Submit New Sensor Data</h3>
      <div class="input-group">
        <label>Temperature (°C):</label>
        <input v-model.number="newData.temperature" type="number" step="0.1" />
      </div>
      <div class="input-group">
        <label>Humidity (%):</label>
        <input v-model.number="newData.humidity" type="number" step="0.1" />
      </div>
      <div class="input-group">
        <label>Air Quality (ppm):</label>
        <input v-model.number="newData.air_quality" type="number" step="0.1" />
      </div>
      <button @click="submitData" :disabled="loading">Submit</button>
    </div>

    <div class="time-window-selector">
      <h3>Select Time Window:</h3>
      <button @click="handleTimeWindowChange('10m')" :class="{ active: timeWindow === '10m' }">
        10 Minutes
      </button>
      <button @click="handleTimeWindowChange('1h')" :class="{ active: timeWindow === '1h' }">
        1 Hour
      </button>
      <button @click="handleTimeWindowChange('24h')" :class="{ active: timeWindow === '24h' }">
        24 Hours
      </button>
    </div>

    <SensorStats :stats="aggregatedStats" />

    <div class="chart-section">
      <h2>Sensor Data Trends</h2>
      <p v-if="sensorData.length === 0">No sensor data available</p>
      <SensorChart v-else :data="sensorData" />
    </div>
  </div>
</template>

<style>
.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: Arial, sans-serif;
}

.loading {
  padding: 1rem;
  background: #f0f0f0;
  border-radius: 4px;
  margin: 1rem 0;
}

.error {
  padding: 1rem;
  background: #ffebee;
  color: #d32f2f;
  border-radius: 4px;
  margin: 1rem 0;
}

.data-input {
  margin: 2rem 0;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 8px;
}

.input-group {
  margin: 0.5rem 0;
}

.input-group label {
  display: inline-block;
  width: 150px;
}

.input-group input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  padding: 0.5rem 1rem;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 0.5rem 0.5rem 0.5rem 0;
}

button:hover {
  background: #369f6b;
}

button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.time-window-selector {
  margin: 1rem 0;
}

.time-window-selector button.active {
  background: #2c3e50;
}

.chart-section {
  margin-top: 2rem;
}
</style>
