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
    <div v-if="!hasValidData" class="no-data-message">
      <p>⚠️ Tidak ada data untuk ditampilkan. Cluster atau members tidak tersedia.</p>
    </div>
    <div v-else class="chart-wrapper">
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

    // Check if we have valid data
    const hasValidData = computed(() => {
      if (!props.clusters || props.clusters.length === 0) {
        console.log('❌ No clusters provided')
        return false
      }
      
      const hasMembers = props.clusters.some(c => c.members && c.members.length > 0)
      if (!hasMembers) {
        console.log('❌ No members in clusters')
        return false
      }
      
      console.log('✅ Valid data:', props.clusters.length, 'clusters')
      return true
    })

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
        console.log('🎨 Creating silhouette chart...')
        console.log('Props clusters:', props.clusters)
        
        if (!chartCanvas.value) {
          console.error('❌ Canvas ref is null')
          return
        }
        
        if (!props.clusters || props.clusters.length === 0) {
          console.error('❌ No clusters data')
          return
        }

        await nextTick()
        
        if (!chartCanvas.value) {
          console.error('❌ Canvas lost after nextTick')
          return
        }

        // Destroy existing chart
        if (chart.value) {
          try {
            chart.value.destroy()
          } catch (e) {
            console.warn('Error destroying chart:', e)
          }
          chart.value = null
        }

        await new Promise(resolve => setTimeout(resolve, 100))
        
        if (!chartCanvas.value) {
          console.error('❌ Canvas lost after delay')
          return
        }

        const ctx = chartCanvas.value.getContext('2d')
        if (!ctx) {
          console.error('❌ Cannot get 2d context')
          return
        }

        console.log('✅ Canvas and context ready')

        // Prepare silhouette data with better spacing
        const datasets = []
        let yPosition = 0
        const gapBetweenClusters = 10 // Fixed gap

        console.log(`Processing ${props.clusters.length} clusters...`)

        props.clusters.forEach((cluster, clusterIndex) => {
          console.log(`Cluster ${cluster.id}:`, cluster.members?.length, 'members')
          
          if (!cluster.members || cluster.members.length === 0) {
            console.warn(`⚠️ Cluster ${cluster.id} has no members`)
            return
          }

          // Calculate silhouette scores for members
          const scores = cluster.members.map(member => ({
            score: calculateApproximateSilhouette(member, cluster, props.clusters),
            name: member.kabupaten_kota || 'Unknown'
          }))

          // Sort by score descending
          scores.sort((a, b) => b.score - a.score)

          const data = scores.map((item, index) => ({
            x: item.score,
            y: yPosition + index,
            name: item.name
          }))

          console.log(`Cluster ${cluster.id} data points:`, data.length)

          datasets.push({
            label: `Cluster ${cluster.id}`,
            data: data,
            backgroundColor: getClusterColor(clusterIndex),
            borderColor: getClusterColor(clusterIndex),
            borderWidth: 1,
            barThickness: 2,
            barPercentage: 1.0,
            categoryPercentage: 1.0
          })

          yPosition += scores.length + gapBetweenClusters
        })

        console.log(`Total datasets: ${datasets.length}, total Y positions: ${yPosition}`)

        if (datasets.length === 0) {
          console.error('❌ No datasets created')
          return
        }

        console.log('✅ Creating chart with', datasets.length, 'datasets')

        const config = {
          type: 'bar',
          data: { datasets },
          options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: {
              title: {
                display: true,
                text: 'Silhouette Plot - Kualitas Clustering per Data Point',
                font: { size: 16, weight: 'bold' },
                color: '#2d3748',
                padding: 20
              },
              legend: {
                display: true,
                position: 'bottom',
                labels: {
                  padding: 15,
                  font: { size: 12 }
                }
              },
              tooltip: {
                enabled: true,
                callbacks: {
                  label: (context) => {
                    const point = context.raw
                    return [
                      `Region: ${point.name || 'N/A'}`,
                      `Score: ${point.x?.toFixed(3) || 'N/A'}`,
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
                  text: 'Silhouette Score',
                  font: { size: 14, weight: 'bold' },
                  color: '#2d3748'
                },
                min: -1,
                max: 1,
                ticks: {
                  font: { size: 11 }
                },
                grid: {
                  display: true,
                  color: (context) => {
                    if (context.tick.value === 0) return 'rgba(0, 0, 0, 0.4)'
                    return 'rgba(0, 0, 0, 0.1)'
                  },
                  lineWidth: (context) => {
                    return context.tick.value === 0 ? 2 : 1
                  }
                }
              },
              y: {
                display: false,
                offset: true
              }
            },
            elements: {
              bar: {
                borderWidth: 0
              }
            }
          }
        }

        console.log('Creating Chart.js instance...')
        chart.value = new Chart(ctx, config)
        console.log('✅ Chart created successfully!')
        console.log('Chart instance:', chart.value)

      } catch (error) {
        console.error('❌ Error creating silhouette plot:', error)
        console.error('Error details:', error.message)
        console.error('Stack:', error.stack)
        if (chart.value) {
          try {
            chart.value.destroy()
          } catch (e) {
            console.error('Error destroying chart:', e)
          }
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
      console.log('📊 SilhouettePlot mounted')
      console.log('Clusters prop:', props.clusters)
      console.log('Has valid data:', hasValidData.value)
      
      if (hasValidData.value) {
        await createChart()
      } else {
        console.warn('⚠️ No valid data to create chart')
      }
    })

    onUnmounted(() => {
      console.log('📊 SilhouettePlot unmounting')
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

    watch(() => props.clusters, (newClusters) => {
      console.log('👀 Clusters changed:', newClusters)
      if (hasValidData.value) {
        updateChart()
      }
    }, { deep: true })

    return {
      chartCanvas,
      averageSilhouetteScore,
      getClusterColor,
      hasValidData
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
  height: 600px;
  position: relative;
  min-height: 400px;
  width: 100%;
}

.silhouette-plot-canvas {
  width: 100% !important;
  height: 100% !important;
}

.no-data-message {
  padding: 3rem 2rem;
  text-align: center;
  background: #f7fafc;
  border-radius: 8px;
  border: 2px dashed #e2e8f0;
  margin: 2rem 0;
}

.no-data-message p {
  color: #718096;
  font-size: 1rem;
  margin: 0;
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
