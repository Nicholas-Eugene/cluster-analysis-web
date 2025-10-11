<template>
  <div class="box-plot-container">
    <div class="chart-header">
      <h3>{{ title }}</h3>
      <div class="chart-controls">
        <select v-model="selectedMetric" @change="updateChart" class="metric-select">
          <option value="ipm">IPM</option>
          <option value="garis_kemiskinan">Garis Kemiskinan</option>
          <option value="pengeluaran_per_kapita">Pengeluaran Per Kapita</option>
        </select>
      </div>
    </div>
    <div class="chart-wrapper">
      <canvas ref="chartCanvas"></canvas>
    </div>
    <div class="statistics-summary">
      <div class="stats-grid">
        <div v-for="(cluster, index) in clusters" :key="cluster.id" class="stat-card">
          <div class="stat-header">
            <div class="stat-color" :style="{ backgroundColor: getClusterColor(index) }"></div>
            <h4>Cluster {{ cluster.id }}</h4>
          </div>
          <div class="stat-values">
            <div class="stat-item">
              <span class="stat-label">Min:</span>
              <span class="stat-value">{{ formatValue(getStatistics(cluster)[selectedMetric].min) }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Q1:</span>
              <span class="stat-value">{{ formatValue(getStatistics(cluster)[selectedMetric].q1) }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Median:</span>
              <span class="stat-value">{{ formatValue(getStatistics(cluster)[selectedMetric].median) }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Q3:</span>
              <span class="stat-value">{{ formatValue(getStatistics(cluster)[selectedMetric].q3) }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Max:</span>
              <span class="stat-value">{{ formatValue(getStatistics(cluster)[selectedMetric].max) }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Mean:</span>
              <span class="stat-value">{{ formatValue(getStatistics(cluster)[selectedMetric].mean) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'BoxPlot',
  props: {
    clusters: {
      type: Array,
      required: true
    },
    title: {
      type: String,
      default: 'Box Plot Analisis per Cluster'
    }
  },
  setup(props) {
    const chartCanvas = ref(null)
    const chart = ref(null)
    const selectedMetric = ref('ipm')

    const colors = [
      '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
      '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
    ]

    const getClusterColor = (index) => {
      return colors[index % colors.length]
    }

    const formatValue = (value) => {
      if (selectedMetric.value === 'garis_kemiskinan' || selectedMetric.value === 'pengeluaran_per_kapita') {
        return new Intl.NumberFormat('id-ID', {
          style: 'currency',
          currency: 'IDR',
          minimumFractionDigits: 0
        }).format(value)
      }
      return value.toFixed(2)
    }

    const calculateStatistics = (values) => {
      const sorted = [...values].sort((a, b) => a - b)
      const n = sorted.length
      
      const min = sorted[0]
      const max = sorted[n - 1]
      const median = n % 2 === 0 
        ? (sorted[n/2 - 1] + sorted[n/2]) / 2 
        : sorted[Math.floor(n/2)]
      
      const q1Index = Math.floor(n * 0.25)
      const q3Index = Math.floor(n * 0.75)
      const q1 = sorted[q1Index]
      const q3 = sorted[q3Index]
      
      const mean = values.reduce((sum, val) => sum + val, 0) / n
      
      return { min, q1, median, q3, max, mean }
    }

    const getStatistics = (cluster) => {
      const metrics = ['ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita']
      const stats = {}
      
      metrics.forEach(metric => {
        const values = cluster.members.map(member => member[metric]).filter(val => val != null)
        stats[metric] = calculateStatistics(values)
      })
      
      return stats
    }

    const createBoxPlotData = () => {
      return props.clusters.map((cluster, index) => {
        const values = cluster.members
          .map(member => member[selectedMetric.value])
          .filter(val => val != null)
        
        const stats = calculateStatistics(values)
        
        return {
          label: `Cluster ${cluster.id}`,
          data: [{
            x: `Cluster ${cluster.id}`,
            y: [stats.min, stats.q1, stats.median, stats.q3, stats.max]
          }],
          backgroundColor: getClusterColor(index) + '80', // Add transparency
          borderColor: getClusterColor(index),
          borderWidth: 2,
          outlierColor: getClusterColor(index),
          outlierBackgroundColor: getClusterColor(index)
        }
      })
    }

    const createChart = async () => {
      try {
        // Multiple validation checks
        if (!chartCanvas.value || !props.clusters || props.clusters.length === 0) return

        // Wait for DOM to be ready
        await nextTick()
        
        // Re-check after nextTick
        if (!chartCanvas.value || !chartCanvas.value.offsetParent) return
        
        // Destroy existing chart first
        if (chart.value) {
          try {
            chart.value.destroy()
          } catch (e) {
            console.warn('Error destroying existing chart:', e)
          }
          chart.value = null
        }
        
        // Get context with additional validation
        const ctx = chartCanvas.value.getContext('2d')
        if (!ctx || !ctx.canvas) return
        
        // Ensure canvas has dimensions
        if (ctx.canvas.width === 0 || ctx.canvas.height === 0) {
          setTimeout(() => createChart(), 100)
          return
        }
      
      // Since Chart.js doesn't have native box plot support, we'll create a custom visualization
      // using bar charts to simulate box plots
      const datasets = props.clusters.map((cluster, index) => {
        const values = cluster.members
          .map(member => member[selectedMetric.value])
          .filter(val => val != null)
        
        const stats = calculateStatistics(values)
        
        return {
          label: `Cluster ${cluster.id}`,
          data: [stats.median], // Show median as the main value
          backgroundColor: getClusterColor(index) + '80',
          borderColor: getClusterColor(index),
          borderWidth: 2,
          // Store additional stats for tooltip
          stats: stats
        }
      })

      const config = {
        type: 'bar',
        data: {
          labels: props.clusters.map(cluster => `Cluster ${cluster.id}`),
          datasets: datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: `Distribusi ${getMetricLabel(selectedMetric.value)} per Cluster`
            },
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                title: (context) => {
                  return context[0].label
                },
                label: (context) => {
                  const stats = context.dataset.stats
                  return [
                    `Min: ${formatValue(stats.min)}`,
                    `Q1: ${formatValue(stats.q1)}`,
                    `Median: ${formatValue(stats.median)}`,
                    `Q3: ${formatValue(stats.q3)}`,
                    `Max: ${formatValue(stats.max)}`,
                    `Mean: ${formatValue(stats.mean)}`
                  ]
                }
              }
            }
          },
          scales: {
            x: {
              title: {
                display: true,
                text: 'Cluster'
              }
            },
            y: {
              title: {
                display: true,
                text: getMetricLabel(selectedMetric.value)
              },
              ticks: {
                callback: function(value) {
                  return formatValue(value)
                }
              }
            }
          }
        }
      }

      chart.value = new Chart(ctx, config)
      
      } catch (error) {
        console.warn('Error creating box plot chart:', error)
        if (chart.value) {
          chart.value.destroy()
          chart.value = null
        }
      }
    }

    const getMetricLabel = (metric) => {
      const labels = {
        'ipm': 'IPM',
        'garis_kemiskinan': 'Garis Kemiskinan (Rp)',
        'pengeluaran_per_kapita': 'Pengeluaran Per Kapita (Rp)'
      }
      return labels[metric] || metric
    }

    const updateChart = () => {
      // Debounce chart updates to prevent rapid recreation
      if (updateChart.timeout) {
        clearTimeout(updateChart.timeout)
      }
      updateChart.timeout = setTimeout(() => {
        createChart()
      }, 100)
    }

    onMounted(async () => {
      await createChart()
    })

    onUnmounted(() => {
      // Clear any pending timeouts
      if (updateChart.timeout) {
        clearTimeout(updateChart.timeout)
      }
      
      if (chart.value) {
        chart.value.destroy()
        chart.value = null
      }
    })

    watch(() => props.clusters, () => {
      updateChart()
    }, { deep: true })

    return {
      chartCanvas,
      selectedMetric,
      getClusterColor,
      getStatistics,
      formatValue,
      updateChart
    }
  }
}
</script>

<style scoped>
.box-plot-container {
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

.metric-select {
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

.statistics-summary {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: #f7fafc;
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid #e2e8f0;
}

.stat-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.stat-color {
  width: 16px;
  height: 16px;
  border-radius: 50%;
}

.stat-header h4 {
  color: #2d3748;
  margin: 0;
  font-size: 1rem;
}

.stat-values {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.25rem 0;
}

.stat-label {
  font-weight: 600;
  color: #4a5568;
  font-size: 0.875rem;
}

.stat-value {
  color: #2d3748;
  font-size: 0.875rem;
  text-align: right;
}

@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .chart-wrapper {
    height: 300px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-values {
    grid-template-columns: 1fr;
  }
}
</style>