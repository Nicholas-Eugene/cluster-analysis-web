<template>
  <div class="silhouette-plot-container">
    <div class="chart-header">
      <h3>{{ title }}</h3>
      <div class="silhouette-info">
        <div class="info-badge">
          <span class="info-icon">ℹ️</span>
          <span class="info-text">Silhouette plot menunjukkan kualitas clustering untuk setiap data point</span>
        </div>
      </div>
    </div>
    <div class="chart-wrapper">
      <canvas ref="chartCanvas" class="silhouette-plot-canvas"></canvas>
    </div>
    <div class="silhouette-legend">
      <h4>Interpretasi Silhouette Score:</h4>
      <div class="legend-items">
        <div class="legend-item">
          <div class="legend-marker excellent"></div>
          <span>> 0.7: Sangat Baik - Data sangat cocok dengan clusternya</span>
        </div>
        <div class="legend-item">
          <div class="legend-marker good"></div>
          <span>0.5 - 0.7: Baik - Data cocok dengan clusternya</span>
        </div>
        <div class="legend-item">
          <div class="legend-marker fair"></div>
          <span>0.25 - 0.5: Cukup - Data cukup cocok dengan clusternya</span>
        </div>
        <div class="legend-item">
          <div class="legend-marker poor"></div>
          <span>< 0.25: Perlu Review - Data mungkin salah cluster</span>
        </div>
      </div>
      <div class="average-score">
        <strong>Average Silhouette Score:</strong> 
        <span class="score-value">{{ averageSilhouetteScore?.toFixed(4) || 'N/A' }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'SilhouettePlot',
  props: {
    clusters: {
      type: Array,
      required: true
    },
    title: {
      type: String,
      default: 'Silhouette Plot - Analisis Kualitas Clustering'
    },
    silhouetteScore: {
      type: Number,
      default: null
    }
  },
  setup(props) {
    const chartCanvas = ref(null)
    const chart = ref(null)

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

    // Calculate silhouette-like approximation based on cluster cohesion
    const calculateApproximateSilhouette = (member, cluster, allClusters) => {
      // Simple approximation: use distance from centroid
      if (!cluster.centroid) return 0.5
      
      const features = ['ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita']
      let distance = 0
      let count = 0
      
      features.forEach(feature => {
        if (member[feature] != null && cluster.centroid[feature] != null) {
          const diff = (member[feature] - cluster.centroid[feature]) / cluster.centroid[feature]
          distance += diff * diff
          count++
        }
      })
      
      if (count === 0) return 0.5
      
      distance = Math.sqrt(distance / count)
      
      // Normalize to silhouette-like score (-1 to 1)
      // Lower distance = higher silhouette score
      return Math.max(-1, Math.min(1, 1 - distance))
    }

    const averageSilhouetteScore = computed(() => {
      if (props.silhouetteScore != null) {
        return props.silhouetteScore
      }
      
      // Calculate approximate average
      let total = 0
      let count = 0
      
      props.clusters.forEach(cluster => {
        cluster.members.forEach(member => {
          const score = calculateApproximateSilhouette(member, cluster, props.clusters)
          total += score
          count++
        })
      })
      
      return count > 0 ? total / count : 0
    })

    const createChart = async () => {
      try {
        if (!chartCanvas.value || !props.clusters || props.clusters.length === 0) {
          return
        }

        await nextTick()
        
        if (!chartCanvas.value) return

        // Destroy existing chart
        if (chart.value) {
          try {
            chart.value.destroy()
          } catch (e) {
            console.warn('Error destroying chart:', e)
          }
          chart.value = null
        }

        await new Promise(resolve => setTimeout(resolve, 50))
        
        if (!chartCanvas.value) return

        const ctx = chartCanvas.value.getContext('2d')
        if (!ctx) return

        // Prepare silhouette data
        const datasets = []
        let yPosition = 0

        props.clusters.forEach((cluster, clusterIndex) => {
          // Calculate silhouette scores for members
          const scores = cluster.members.map(member => ({
            score: calculateApproximateSilhouette(member, cluster, props.clusters),
            name: member.kabupaten_kota
          }))

          // Sort by score descending
          scores.sort((a, b) => b.score - a.score)

          const data = scores.map((item, index) => ({
            x: item.score,
            y: yPosition + index,
            name: item.name
          }))

          datasets.push({
            label: `Cluster ${cluster.id}`,
            data: data,
            backgroundColor: getClusterColor(clusterIndex),
            borderColor: getClusterColor(clusterIndex),
            borderWidth: 1,
            barThickness: 2
          })

          yPosition += scores.length + 2 // Add gap between clusters
        })

        const config = {
          type: 'bar',
          data: { datasets },
          options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 0 },
            plugins: {
              title: {
                display: true,
                text: 'Silhouette Plot - Kualitas Clustering per Data Point',
                font: { size: 14, weight: 'bold' }
              },
              legend: {
                display: true,
                position: 'bottom'
              },
              tooltip: {
                callbacks: {
                  label: (context) => {
                    const point = context.raw
                    return [
                      `Region: ${point.name}`,
                      `Silhouette Score: ${point.x?.toFixed(3) || 'N/A'}`,
                      context.dataset.label
                    ]
                  }
                }
              }
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: 'Silhouette Score'
                },
                min: -1,
                max: 1,
                grid: {
                  color: (context) => {
                    if (context.tick.value === 0) return 'rgba(0, 0, 0, 0.3)'
                    return 'rgba(0, 0, 0, 0.1)'
                  },
                  lineWidth: (context) => {
                    return context.tick.value === 0 ? 2 : 1
                  }
                }
              },
              y: {
                display: false
              }
            }
          }
        }

        chart.value = new Chart(ctx, config)

      } catch (error) {
        console.warn('Error creating silhouette plot:', error)
        if (chart.value) {
          try {
            chart.value.destroy()
          } catch (e) {}
          chart.value = null
        }
      }
    }

    let updateTimeout = null
    let isUpdating = false

    const updateChart = () => {
      if (isUpdating) return
      
      if (updateTimeout) {
        clearTimeout(updateTimeout)
      }
      
      updateTimeout = setTimeout(async () => {
        if (!chartCanvas.value) return
        
        isUpdating = true
        try {
          await createChart()
        } catch (error) {
          console.error('Error during chart update:', error)
        } finally {
          isUpdating = false
        }
      }, 300)
    }

    onMounted(async () => {
      await createChart()
    })

    onUnmounted(() => {
      if (updateTimeout) {
        clearTimeout(updateTimeout)
        updateTimeout = null
      }
      
      isUpdating = true
      
      if (chart.value) {
        try {
          chart.value.destroy()
        } catch (e) {}
        chart.value = null
      }
      
      chartCanvas.value = null
    })

    watch(() => props.clusters, () => {
      updateChart()
    }, { deep: true })

    return {
      chartCanvas,
      averageSilhouetteScore,
      getClusterColor
    }
  }
}
</script>

<style scoped>
.silhouette-plot-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.chart-header {
  margin-bottom: 1rem;
}

.chart-header h3 {
  color: #2d3748;
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
}

.silhouette-info {
  margin-top: 0.5rem;
}

.info-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #f7fafc;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border-left: 3px solid #667eea;
  font-size: 0.9rem;
  color: #4a5568;
}

.info-icon {
  font-size: 1rem;
}

.chart-wrapper {
  height: 400px;
  position: relative;
}

.silhouette-legend {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.silhouette-legend h4 {
  color: #2d3748;
  margin: 0 0 1rem 0;
  font-size: 1rem;
}

.legend-items {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #4a5568;
  padding: 0.5rem;
  background: #f7fafc;
  border-radius: 6px;
}

.legend-marker {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  flex-shrink: 0;
}

.legend-marker.excellent {
  background: #38a169;
}

.legend-marker.good {
  background: #3182ce;
}

.legend-marker.fair {
  background: #d69e2e;
}

.legend-marker.poor {
  background: #e53e3e;
}

.average-score {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  font-size: 1rem;
}

.score-value {
  font-size: 1.5rem;
  font-weight: 700;
  margin-left: 0.5rem;
}

@media (max-width: 768px) {
  .chart-wrapper {
    height: 300px;
  }
  
  .legend-items {
    grid-template-columns: 1fr;
  }
}
</style>
