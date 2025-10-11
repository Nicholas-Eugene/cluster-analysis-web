<template>
  <div class="scatter-plot-container">
    <div class="chart-header">
      <h3>{{ title }}</h3>
      <div class="chart-controls">
        <select v-model="selectedXAxis" @change="updateChart" class="axis-select">
          <option value="ipm">IPM</option>
          <option value="garis_kemiskinan">Garis Kemiskinan</option>
          <option value="pengeluaran_per_kapita">Pengeluaran Per Kapita</option>
        </select>
        <span>vs</span>
        <select v-model="selectedYAxis" @change="updateChart" class="axis-select">
          <option value="ipm">IPM</option>
          <option value="garis_kemiskinan">Garis Kemiskinan</option>
          <option value="pengeluaran_per_kapita">Pengeluaran Per Kapita</option>
        </select>
      </div>
    </div>
    <div class="chart-wrapper">
      <canvas ref="chartCanvas"></canvas>
    </div>
    <div class="chart-legend">
      <div v-for="(cluster, index) in clusters" :key="cluster.id" class="legend-item">
        <div class="legend-color" :style="{ backgroundColor: getClusterColor(index) }"></div>
        <span>Cluster {{ cluster.id }} ({{ cluster.size }} daerah)</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'ScatterPlot',
  props: {
    clusters: {
      type: Array,
      required: true
    },
    title: {
      type: String,
      default: 'Scatter Plot Clustering'
    }
  },
  setup(props) {
    const chartCanvas = ref(null)
    const chart = ref(null)
    const selectedXAxis = ref('ipm')
    const selectedYAxis = ref('garis_kemiskinan')

    const colors = [
      '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
      '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
    ]

    const getClusterColor = (index) => {
      return colors[index % colors.length]
    }

    const formatAxisLabel = (axis) => {
      const labels = {
        'ipm': 'IPM',
        'garis_kemiskinan': 'Garis Kemiskinan (Rp)',
        'pengeluaran_per_kapita': 'Pengeluaran Per Kapita (Rp)'
      }
      return labels[axis] || axis
    }

    const formatValue = (value, axis) => {
      if (axis === 'garis_kemiskinan' || axis === 'pengeluaran_per_kapita') {
        return new Intl.NumberFormat('id-ID', {
          style: 'currency',
          currency: 'IDR',
          minimumFractionDigits: 0
        }).format(value)
      }
      return value.toFixed(2)
    }

    const createChart = async () => {
      if (!chartCanvas.value || !props.clusters) return

      // Wait for DOM to be ready
      await nextTick()
      
      if (!chartCanvas.value) return
      
      const ctx = chartCanvas.value.getContext('2d')
      if (!ctx) return
      
      // Prepare datasets
      const datasets = props.clusters.map((cluster, index) => {
        const data = cluster.members.map(member => ({
          x: member[selectedXAxis.value],
          y: member[selectedYAxis.value],
          label: member.kabupaten_kota,
          membership: member.membership || 1.0
        }))

        return {
          label: `Cluster ${cluster.id}`,
          data: data,
          backgroundColor: getClusterColor(index),
          borderColor: getClusterColor(index),
          borderWidth: 2,
          pointRadius: (ctx) => {
            // Size based on membership for FCM
            const membership = ctx.parsed?.membership || 1.0
            return Math.max(4, membership * 8)
          },
          pointHoverRadius: 8
        }
      })

      const config = {
        type: 'scatter',
        data: { datasets },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: `${formatAxisLabel(selectedXAxis.value)} vs ${formatAxisLabel(selectedYAxis.value)}`
            },
            legend: {
              display: false // We'll use custom legend
            },
            tooltip: {
              callbacks: {
                title: (context) => {
                  return context[0].raw.label
                },
                label: (context) => {
                  const point = context.raw
                  const lines = [
                    `${formatAxisLabel(selectedXAxis.value)}: ${formatValue(point.x, selectedXAxis.value)}`,
                    `${formatAxisLabel(selectedYAxis.value)}: ${formatValue(point.y, selectedYAxis.value)}`
                  ]
                  if (point.membership && point.membership < 1.0) {
                    lines.push(`Membership: ${(point.membership * 100).toFixed(1)}%`)
                  }
                  return lines
                }
              }
            }
          },
          scales: {
            x: {
              title: {
                display: true,
                text: formatAxisLabel(selectedXAxis.value)
              },
              ticks: {
                callback: function(value) {
                  return formatValue(value, selectedXAxis.value)
                }
              }
            },
            y: {
              title: {
                display: true,
                text: formatAxisLabel(selectedYAxis.value)
              },
              ticks: {
                callback: function(value) {
                  return formatValue(value, selectedYAxis.value)
                }
              }
            }
          },
          interaction: {
            intersect: false,
            mode: 'point'
          }
        }
      }

      if (chart.value) {
        chart.value.destroy()
      }

      chart.value = new Chart(ctx, config)
    }

    const updateChart = () => {
      createChart()
    }

    onMounted(async () => {
      await createChart()
    })

    onUnmounted(() => {
      if (chart.value) {
        chart.value.destroy()
      }
    })

    watch(() => props.clusters, async () => {
      await createChart()
    }, { deep: true })

    return {
      chartCanvas,
      selectedXAxis,
      selectedYAxis,
      getClusterColor,
      updateChart
    }
  }
}
</script>

<style scoped>
.scatter-plot-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.chart-header h3 {
  color: #2d3748;
  margin: 0;
  font-size: 1.25rem;
}

.chart-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.axis-select {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: white;
  color: #4a5568;
  font-size: 0.875rem;
}

.chart-wrapper {
  height: 400px;
  position: relative;
}

.chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #4a5568;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .chart-controls {
    justify-content: center;
  }
  
  .chart-wrapper {
    height: 300px;
  }
  
  .chart-legend {
    justify-content: center;
  }
}
</style>