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
      <canvas ref="chartCanvas" class="box-plot-canvas"></canvas>
    </div>
    <div class="statistics-summary">
      <div class="stats-grid">
        <div v-for="(cluster, index) in clusters" :key="`cluster-${cluster.id}`" class="stat-card">
          <div class="stat-header">
            <div class="stat-color" :style="{ backgroundColor: getClusterColor(index) }"></div>
            <h4>{{ getClusterLabel(cluster) }}</h4>
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
import { BoxPlotController, BoxAndWiskers } from '@sgratzl/chartjs-chart-boxplot'

// Register the box plot controller
Chart.register(BoxPlotController, BoxAndWiskers)

export default {
  name: 'BoxPlot',
  props: {
    clusters: {
      type: Array,
      required: true
    },
    title: {
      type: String,
      default: 'Box and Whisker Plot - Analisis Distribusi per Cluster'
    }
  },
  setup(props) {
    const chartCanvas = ref(null)
    const chart = ref(null)
    const selectedMetric = ref('ipm')

    // Consistent cluster colors matching the design system
    const colors = [
      '#667eea', // Purple - Primary
      '#48bb78', // Green - Success
      '#ed8936', // Orange - Warning
      '#4299e1', // Blue - Info
      '#f56565', // Red - Danger
      '#38b2ac', // Teal
      '#9f7aea', // Purple Light
      '#ecc94b', // Yellow
      '#f687b3', // Pink
      '#4fd1c5', // Cyan
    ]

    const getClusterColor = (index) => {
      return colors[index % colors.length]
    }
    
    // Safe cluster label getter (handles noise clusters and object interpretation)
    const getClusterLabel = (cluster) => {
      if (!cluster) return 'Unknown'
      if (cluster.id === -1 || cluster.id === '-1') {
        return 'Noise (Outliers)'
      }
      // Ensure we get a clean string, not an object
      if (cluster.interpretation && cluster.interpretation.label) {
        return String(cluster.interpretation.label)
      }
      return `Cluster ${cluster.id}`
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

    const calculateOutliers = (values, stats) => {
      const iqr = stats.q3 - stats.q1
      const lowerBound = stats.q1 - 1.5 * iqr
      const upperBound = stats.q3 + 1.5 * iqr
      return values.filter(v => v < lowerBound || v > upperBound)
    }

    const createBoxPlotData = () => {
      return props.clusters.map((cluster, index) => {
        const values = cluster.members
          .map(member => member[selectedMetric.value])
          .filter(val => val != null)
        
        const stats = calculateStatistics(values)
        const outliers = calculateOutliers(values, stats)
        
        return {
          label: `Cluster ${cluster.id}`,
          data: [values],
          backgroundColor: getClusterColor(index) + 'B3', // 70% opacity
          borderColor: getClusterColor(index),
          borderWidth: 2,
          outlierColor: getClusterColor(index),
          outlierBackgroundColor: getClusterColor(index) + '80',
          outlierBorderColor: getClusterColor(index),
          outlierRadius: 4,
          itemRadius: 0,
          itemStyle: 'circle',
          itemBackgroundColor: getClusterColor(index) + '40'
        }
      })
    }

    const createChart = async () => {
      try {
        // Early validation - check if component is still mounted
        if (!chartCanvas.value) {
          console.warn('Chart canvas ref is null, component may be unmounted')
          return
        }
        
        // Check if we have data to display
        if (!props.clusters || props.clusters.length === 0) {
          console.warn('No cluster data available for chart')
          return
        }

        // Wait for DOM to be fully ready
        await nextTick()
        
        // Re-validate after nextTick - component might have unmounted
        if (!chartCanvas.value) {
          console.warn('Chart canvas became null after nextTick')
          return
        }
        
        // Check if canvas is actually in the DOM and visible
        if (!chartCanvas.value.offsetParent && chartCanvas.value.style.display !== 'none') {
          console.warn('Canvas not visible in DOM, retrying...')
          setTimeout(() => createChart(), 200)
          return
        }
        
        // Destroy existing chart safely
        if (chart.value) {
          try {
            if (typeof chart.value.destroy === 'function') {
              chart.value.destroy()
            }
          } catch (e) {
            console.warn('Error destroying existing chart:', e)
          }
          chart.value = null
        }
        
        // Additional wait to ensure canvas is stable
        await new Promise(resolve => setTimeout(resolve, 50))
        
        // Final validation before getting context
        if (!chartCanvas.value) {
          console.warn('Canvas became null during chart creation')
          return
        }
        
        // Get context with comprehensive validation
        let ctx
        try {
          ctx = chartCanvas.value.getContext('2d')
        } catch (e) {
          console.error('Failed to get 2d context:', e)
          return
        }
        
        if (!ctx || !ctx.canvas) {
          console.warn('Invalid canvas context')
          return
        }
        
        // Ensure canvas has proper dimensions
        const canvas = ctx.canvas
        if (canvas.width === 0 || canvas.height === 0) {
          console.warn('Canvas has zero dimensions, retrying...')
          setTimeout(() => createChart(), 200)
          return
        }
        
        // Check if canvas is still attached to DOM
        if (!document.contains(canvas)) {
          console.warn('Canvas is not attached to DOM')
          return
        }
      
      // Create box and whisker plot visualization with proper structure
      const labels = props.clusters.map(cluster => `Cluster ${cluster.id}`)
      const datasets = [{
        label: 'Clusters',
        data: props.clusters.map((cluster, index) => {
          const values = cluster.members
            .map(member => member[selectedMetric.value])
            .filter(val => val != null)
          return values
        }),
        backgroundColor: props.clusters.map((cluster, index) => getClusterColor(index) + 'B3'),
        borderColor: props.clusters.map((cluster, index) => getClusterColor(index)),
        borderWidth: 2,
        outlierColor: props.clusters.map((cluster, index) => getClusterColor(index)),
        outlierBackgroundColor: props.clusters.map((cluster, index) => getClusterColor(index) + '80'),
        outlierBorderColor: props.clusters.map((cluster, index) => getClusterColor(index)),
        outlierRadius: 4,
        itemRadius: 0
      }]

      const config = {
        type: 'boxplot',
        data: {
          labels: labels,
          datasets: datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          // Disable animations to prevent timing issues
          animation: {
            duration: 0
          },
          // Disable hover animations
          hover: {
            animationDuration: 0
          },
          // Disable responsiveAnimationDuration
          responsiveAnimationDuration: 0,
          plugins: {
            title: {
              display: true,
              text: `Box and Whisker Plot - ${getMetricLabel(selectedMetric.value)} per Cluster`,
              font: {
                size: 14,
                weight: 'bold'
              }
            },
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  const dataIndex = context.dataIndex
                  const cluster = props.clusters[dataIndex]
                  const values = cluster.members
                    .map(member => member[selectedMetric.value])
                    .filter(val => val != null)
                  const stats = calculateStatistics(values)
                  
                  return [
                    `Cluster ${cluster.id}`,
                    `Min: ${formatValue(stats.min)}`,
                    `Q1: ${formatValue(stats.q1)}`,
                    `Median: ${formatValue(stats.median)}`,
                    `Q3: ${formatValue(stats.q3)}`,
                    `Max: ${formatValue(stats.max)}`,
                    `Count: ${values.length}`
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
          try {
            if (typeof chart.value.destroy === 'function') {
              chart.value.destroy()
            }
          } catch (destroyError) {
            console.warn('Error destroying chart after creation error:', destroyError)
          }
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

    let updateTimeout = null
    let isUpdating = false
    
    const updateChart = () => {
      // Prevent multiple simultaneous updates
      if (isUpdating) {
        console.warn('Chart update already in progress, skipping')
        return
      }
      
      // Clear any pending updates
      if (updateTimeout) {
        clearTimeout(updateTimeout)
      }
      
      // Debounce chart updates with longer delay to prevent rapid recreation
      updateTimeout = setTimeout(async () => {
        if (!chartCanvas.value) {
          console.warn('Canvas not available for update')
          return
        }
        
        isUpdating = true
        try {
          await createChart()
        } catch (error) {
          console.error('Error during chart update:', error)
        } finally {
          isUpdating = false
        }
      }, 300) // Increased debounce time
    }

    onMounted(async () => {
      await createChart()
    })

    onUnmounted(() => {
      // Clear any pending timeouts
      if (updateTimeout) {
        clearTimeout(updateTimeout)
        updateTimeout = null
      }
      
      // Set updating flag to prevent any ongoing operations
      isUpdating = true
      
      // Destroy chart safely
      if (chart.value) {
        try {
          if (typeof chart.value.destroy === 'function') {
            chart.value.destroy()
          }
        } catch (e) {
          console.warn('Error destroying chart on unmount:', e)
        }
        chart.value = null
      }
      
      // Clear canvas reference
      chartCanvas.value = null
    })

    watch(() => props.clusters, (newClusters) => {
      console.log('📊 BoxPlot received new clusters:', newClusters)
      if (newClusters && newClusters.length > 0) {
        console.log(`BoxPlot: ${newClusters.length} clusters received`)
        newClusters.forEach((cluster, index) => {
          console.log(`  Cluster ${cluster.id}: ${cluster.size} members`)
        })
      } else {
        console.log('BoxPlot: No clusters received or empty clusters')
      }
      updateChart()
    }, { deep: true })

    return {
      chartCanvas,
      selectedMetric,
      getClusterColor,
      getClusterLabel,
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