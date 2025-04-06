<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { Chart, registerables } from 'chart.js'
import type { SensorData } from '@/types/sensor'

Chart.register(...registerables)

const props = defineProps<{
  data: SensorData[]
}>()

let chart: Chart | null = null

const initChart = (canvas: HTMLCanvasElement) => {
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: props.data.map((d) => new Date(d.timestamp).toLocaleTimeString()),
      datasets: [
        {
          label: 'Temperature (°C)',
          data: props.data.map((d) => d.temperature !== null ? d.temperature : null),
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
          tension: 0.1,
          pointRadius: (ctx) => (props.data[ctx.dataIndex]?.is_anomaly ? 6 : 3),
          pointBackgroundColor: (ctx) =>
            props.data[ctx.dataIndex]?.is_anomaly ? 'rgb(255, 0, 0)' : 'rgb(255, 99, 132)',
          spanGaps: true,  // This will connect lines across null values
        },
        {
          label: 'Humidity (%)',
          data: props.data.map((d) => d.humidity !== null ? d.humidity : null),
          borderColor: 'rgb(54, 162, 235)',
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          tension: 0.1,
          pointRadius: (ctx) => (props.data[ctx.dataIndex]?.is_anomaly ? 6 : 3),
          pointBackgroundColor: (ctx) =>
            props.data[ctx.dataIndex]?.is_anomaly ? 'rgb(255, 0, 0)' : 'rgb(54, 162, 235)',
          spanGaps: true,
        },
        {
          label: 'Air Quality (ppm)',
          data: props.data.map((d) => d.air_quality !== null ? d.air_quality : null),
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.5)',
          tension: 0.1,
          pointRadius: (ctx) => (props.data[ctx.dataIndex]?.is_anomaly ? 6 : 3),
          pointBackgroundColor: (ctx) =>
            props.data[ctx.dataIndex]?.is_anomaly ? 'rgb(255, 0, 0)' : 'rgb(75, 192, 192)',
          spanGaps: true,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          callbacks: {
            afterLabel: (context) => {
              const index = context.dataIndex
              const data = props.data[index]
              return data.is_anomaly ? '⚠️ Anomaly detected' : ''
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: false,
        },
      },
    },
  })
}

onMounted(() => {
  const canvas = document.getElementById('sensorChart') as HTMLCanvasElement
  if (canvas) initChart(canvas)
})

watch(
  () => props.data,
  (newData) => {
    if (chart && newData.length) {
      chart.data.labels = newData.map((d) => new Date(d.timestamp).toLocaleTimeString())
      chart.data.datasets[0].data = newData.map((d) => d.temperature !== null ? d.temperature : null)
      chart.data.datasets[1].data = newData.map((d) => d.humidity !== null ? d.humidity : null)
      chart.data.datasets[2].data = newData.map((d) => d.air_quality !== null ? d.air_quality : null)
      chart.update()
    }
  },
  { deep: true },
)
</script>

<template>
  <div class="chart-container">
    <canvas id="sensorChart"></canvas>
  </div>
</template>

<style scoped>
.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}
</style>