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
      <canvas ref="chartCanvas" class="scatter-plot-canvas"></canvas>
    </div>
    <div class="chart-legend">
      <div v-for="(cluster, index) in clusters" :key="`legend-${cluster.id}`" class="legend-item">
        <div class="legend-color" :style="{ backgroundColor: getClusterColor(index) }"></div>
        <span>{{ getClusterLabel(cluster) }} ({{ cluster.size }} daerah)</span>
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
      
      // Prepare datasets
      const datasets = props.clusters.map((cluster, index) => {
        const data = cluster.members.map(member => ({
          x: member[selectedXAxis.value],
          y: member[selectedYAxis.value],
          label: member.kabupaten_kota,
          membership: member.membership || 1.0
        }))

        // Ensure label is always a clean string (no objects, no special chars)
        const clusterLabel = cluster.interpretation?.label 
          ? String(cluster.interpretation.label) 
          : `Cluster ${cluster.id}`
        
        return {
          label: clusterLabel,
          data: data,
          backgroundColor: getClusterColor(index),
          borderColor: '#ffffff',
          borderWidth: 2,
          pointRadius: (ctx) => {
            // Size based on membership for FCM
            const membership = ctx.parsed?.membership || 1.0
            return Math.max(4, membership * 8)
          },
          pointHoverRadius: 8,
          pointHoverBorderColor: '#ffffff',
          pointHoverBorderWidth: 3
        }
      })

      const config = {
        type: 'scatter',
        data: { datasets },
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

      chart.value = new Chart(ctx, config)
      
      } catch (error) {
        console.warn('Error creating scatter plot chart:', error)
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
      console.log('📈 ScatterPlot received new clusters:', newClusters)
      if (newClusters && newClusters.length > 0) {
        console.log(`ScatterPlot: ${newClusters.length} clusters received`)
        newClusters.forEach((cluster, index) => {
          console.log(`  Cluster ${cluster.id}: ${cluster.size} members`)
        })
      } else {
        console.log('ScatterPlot: No clusters received or empty clusters')
      }
      updateChart()
    }, { deep: true })

    return {
      chartCanvas,
      selectedXAxis,
      selectedYAxis,
      getClusterColor,
      getClusterLabel,
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