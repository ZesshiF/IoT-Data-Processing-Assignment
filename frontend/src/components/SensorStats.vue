<script setup lang="ts">
import type { AggregatedStats } from '@/types/sensor'

const props = defineProps<{
  stats: AggregatedStats | null
}>()

const timeWindowLabel = (window: string) => {
  switch (window) {
    case '10m':
      return 'Last 10 minutes'
    case '1h':
      return 'Last hour'
    case '24h':
      return 'Last 24 hours'
    default:
      return window
  }
}
</script>

<template>
  <div v-if="stats" class="stats-container">
    <h3>{{ timeWindowLabel(stats.time_window) }} Statistics</h3>

    <div class="stats-grid">
      <div class="stat-card">
        <h4>Temperature (°C)</h4>
        <p>Mean: {{ stats.temperature_mean.toFixed(2) }}</p>
        <p>Median: {{ stats.temperature_median.toFixed(2) }}</p>
        <p>Min: {{ stats.temperature_min.toFixed(2) }}</p>
        <p>Max: {{ stats.temperature_max.toFixed(2) }}</p>
      </div>

      <div class="stat-card">
        <h4>Humidity (%)</h4>
        <p>Mean: {{ stats.humidity_mean.toFixed(2) }}</p>
        <p>Median: {{ stats.humidity_median.toFixed(2) }}</p>
        <p>Min: {{ stats.humidity_min.toFixed(2) }}</p>
        <p>Max: {{ stats.humidity_max.toFixed(2) }}</p>
      </div>

      <div class="stat-card">
        <h4>Air Quality (ppm)</h4>
        <p>Mean: {{ stats.air_quality_mean.toFixed(2) }}</p>
        <p>Median: {{ stats.air_quality_median.toFixed(2) }}</p>
        <p>Min: {{ stats.air_quality_min.toFixed(2) }}</p>
        <p>Max: {{ stats.air_quality_max.toFixed(2) }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stats-container {
  margin-top: 2rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 8px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.stat-card {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-card h4 {
  margin-top: 0;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}

.stat-card p {
  margin: 0.5rem 0;
  color: #666;
}
</style>
