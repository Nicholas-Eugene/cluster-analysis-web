<template>
  <div class="correlation-matrix-container">
    <div class="chart-header">
      <h3>{{ title }}</h3>
      <div class="chart-info">
        <p>Matriks korelasi menunjukkan hubungan antar variabel. Nilai mendekati 1 menunjukkan korelasi positif kuat, nilai mendekati -1 menunjukkan korelasi negatif kuat.</p>
      </div>
    </div>
    <div class="chart-wrapper">
      <canvas ref="chartCanvas" class="correlation-canvas"></canvas>
    </div>
    <div class="correlation-legend">
      <div class="legend-scale">
        <div class="scale-item">
          <div class="color-box" style="background: #d73027;"></div>
          <span>-1.0 (Korelasi Negatif Kuat)</span>
        </div>
        <div class="scale-item">
          <div class="color-box" style="background: #f46d43;"></div>
          <span>-0.5</span>
        </div>
        <div class="scale-item">
          <div class="color-box" style="background: #fdae61;"></div>
          <span>0.0 (Tidak Ada Korelasi)</span>
        </div>
        <div class="scale-item">
          <div class="color-box" style="background: #abd9e9;"></div>
          <span>0.5</span>
        </div>
        <div class="scale-item">
          <div class="color-box" style="background: #2166ac;"></div>
          <span>1.0 (Korelasi Positif Kuat)</span>
        </div>
      </div>
    </div>
    <div class="correlation-insights">
      <h4>📊 Insight Korelasi</h4>
      <div class="insights-grid">
        <div v-for="insight in correlationInsights" :key="insight.pair" class="insight-card">
          <div class="insight-header">
            <span class="insight-variables">{{ insight.pair }}</span>
            <span class="insight-value" :class="getCorrelationClass(insight.correlation)">
              {{ insight.correlation.toFixed(3) }}
            </span>
          </div>
          <p class="insight-description">{{ insight.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'CorrelationMatrix',
  props: {
    clusters: {
      type: Array,
      required: true
    },
    title: {
      type: String,
      default: 'Analisis Korelasi Variabel'
    }
  },
  setup(props) {
    const chartCanvas = ref(null)
    const chart = ref(null)

    const variables = ['ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita']
    const variableLabels = {
      'ipm': 'IPM',
      'garis_kemiskinan': 'Garis Kemiskinan',
      'pengeluaran_per_kapita': 'Pengeluaran Per Kapita'
    }

    const getAllData = () => {
      const allData = []
      props.clusters.forEach(cluster => {
        cluster.members.forEach(member => {
          allData.push(member)
        })
      })
      return allData
    }

    const calculateCorrelation = (x, y) => {
      const n = x.length
      if (n === 0) return 0

      const sumX = x.reduce((a, b) => a + b, 0)
      const sumY = y.reduce((a, b) => a + b, 0)
      const sumXY = x.reduce((sum, xi, i) => sum + xi * y[i], 0)
      const sumX2 = x.reduce((sum, xi) => sum + xi * xi, 0)
      const sumY2 = y.reduce((sum, yi) => sum + yi * yi, 0)

      const numerator = n * sumXY - sumX * sumY
      const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY))

      return denominator === 0 ? 0 : numerator / denominator
    }

    const correlationMatrix = computed(() => {
      const data = getAllData()
      const matrix = []

      variables.forEach((var1, i) => {
        matrix[i] = []
        variables.forEach((var2, j) => {
          if (i === j) {
            matrix[i][j] = 1
          } else {
            const values1 = data.map(d => d[var1]).filter(v => v != null)
            const values2 = data.map(d => d[var2]).filter(v => v != null)
            
            // Ensure both arrays have the same length
            const minLength = Math.min(values1.length, values2.length)
            const x = values1.slice(0, minLength)
            const y = values2.slice(0, minLength)
            
            matrix[i][j] = calculateCorrelation(x, y)
          }
        })
      })

      return matrix
    })

    const correlationInsights = computed(() => {
      const insights = []
      const matrix = correlationMatrix.value

      variables.forEach((var1, i) => {
        variables.forEach((var2, j) => {
          if (i < j) { // Only process upper triangle to avoid duplicates
            const correlation = matrix[i][j]
            const pair = `${variableLabels[var1]} vs ${variableLabels[var2]}`
            
            let description = ''
            const absCorr = Math.abs(correlation)
            
            if (absCorr >= 0.8) {
              description = correlation > 0 ? 
                'Korelasi positif sangat kuat - kedua variabel bergerak searah dengan hubungan yang sangat erat.' :
                'Korelasi negatif sangat kuat - kedua variabel bergerak berlawanan arah dengan hubungan yang sangat erat.'
            } else if (absCorr >= 0.6) {
              description = correlation > 0 ? 
                'Korelasi positif kuat - kedua variabel cenderung bergerak searah.' :
                'Korelasi negatif kuat - kedua variabel cenderung bergerak berlawanan arah.'
            } else if (absCorr >= 0.4) {
              description = correlation > 0 ? 
                'Korelasi positif sedang - ada hubungan positif yang cukup signifikan.' :
                'Korelasi negatif sedang - ada hubungan negatif yang cukup signifikan.'
            } else if (absCorr >= 0.2) {
              description = correlation > 0 ? 
                'Korelasi positif lemah - hubungan positif yang tidak terlalu kuat.' :
                'Korelasi negatif lemah - hubungan negatif yang tidak terlalu kuat.'
            } else {
              description = 'Korelasi sangat lemah atau tidak ada hubungan linear yang signifikan.'
            }

            insights.push({
              pair,
              correlation,
              description
            })
          }
        })
      })

      return insights.sort((a, b) => Math.abs(b.correlation) - Math.abs(a.correlation))
    })

    const getCorrelationColor = (value) => {
      // Color scale from red (negative) to blue (positive)
      const absValue = Math.abs(value)
      if (value > 0) {
        // Positive correlation: white to blue
        const intensity = Math.floor(absValue * 255)
        return `rgb(${255 - intensity}, ${255 - intensity}, 255)`
      } else {
        // Negative correlation: white to red
        const intensity = Math.floor(absValue * 255)
        return `rgb(255, ${255 - intensity}, ${255 - intensity})`
      }
    }

    const getCorrelationClass = (value) => {
      const absValue = Math.abs(value)
      if (absValue >= 0.8) return 'correlation-very-strong'
      if (absValue >= 0.6) return 'correlation-strong'
      if (absValue >= 0.4) return 'correlation-moderate'
      if (absValue >= 0.2) return 'correlation-weak'
      return 'correlation-very-weak'
    }

    const createChart = async () => {
      try {
        if (!chartCanvas.value) {
          console.warn('CorrelationMatrix: Chart canvas ref is null')
          return
        }

        if (!props.clusters || props.clusters.length === 0) {
          console.warn('CorrelationMatrix: No cluster data available')
          return
        }

        await nextTick()

        if (!chartCanvas.value) {
          console.warn('CorrelationMatrix: Chart canvas became null after nextTick')
          return
        }

        if (chart.value) {
          try {
            chart.value.destroy()
          } catch (e) {
            console.warn('CorrelationMatrix: Error destroying existing chart:', e)
          }
          chart.value = null
        }

        await new Promise(resolve => setTimeout(resolve, 50))

        if (!chartCanvas.value) {
          console.warn('CorrelationMatrix: Canvas became null during chart creation')
          return
        }

        let ctx
        try {
          ctx = chartCanvas.value.getContext('2d')
        } catch (e) {
          console.error('CorrelationMatrix: Failed to get 2d context:', e)
          return
        }

        if (!ctx || !ctx.canvas) {
          console.warn('CorrelationMatrix: Invalid canvas context')
          return
        }

        const canvas = ctx.canvas
        if (canvas.width === 0 || canvas.height === 0) {
          console.warn('CorrelationMatrix: Canvas has zero dimensions, retrying...')
          setTimeout(() => createChart(), 200)
          return
        }

        if (!document.contains(canvas)) {
          console.warn('CorrelationMatrix: Canvas is not attached to DOM')
          return
        }

        try {
          ctx.save()
          ctx.restore()
        } catch (contextError) {
          console.error('CorrelationMatrix: Canvas context is invalid:', contextError)
          return
        }

        // Create heatmap data
        const matrix = correlationMatrix.value
        const heatmapData = []

        variables.forEach((var1, i) => {
          variables.forEach((var2, j) => {
            heatmapData.push({
              x: variableLabels[var2],
              y: variableLabels[var1],
              v: matrix[i][j]
            })
          })
        })

        const config = {
          type: 'scatter',
          data: {
            datasets: [{
              label: 'Correlation',
              data: heatmapData,
              backgroundColor: (ctx) => {
                const value = ctx.parsed.v
                return getCorrelationColor(value)
              },
              borderColor: '#333',
              borderWidth: 1,
              pointRadius: 40,
              pointHoverRadius: 45
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 0 },
            hover: { animationDuration: 0 },
            responsiveAnimationDuration: 0,
            plugins: {
              title: {
                display: true,
                text: 'Matriks Korelasi Variabel Clustering'
              },
              legend: {
                display: false
              },
              tooltip: {
                callbacks: {
                  title: (context) => {
                    const point = context[0]
                    return `${point.parsed.y} vs ${point.parsed.x}`
                  },
                  label: (context) => {
                    const value = context.parsed.v
                    const strength = Math.abs(value) >= 0.8 ? 'Sangat Kuat' :
                                   Math.abs(value) >= 0.6 ? 'Kuat' :
                                   Math.abs(value) >= 0.4 ? 'Sedang' :
                                   Math.abs(value) >= 0.2 ? 'Lemah' : 'Sangat Lemah'
                    const direction = value > 0 ? 'Positif' : value < 0 ? 'Negatif' : 'Netral'
                    return [
                      `Korelasi: ${value.toFixed(3)}`,
                      `Kekuatan: ${strength}`,
                      `Arah: ${direction}`
                    ]
                  }
                }
              }
            },
            scales: {
              x: {
                type: 'category',
                position: 'bottom',
                title: {
                  display: true,
                  text: 'Variabel'
                }
              },
              y: {
                type: 'category',
                title: {
                  display: true,
                  text: 'Variabel'
                }
              }
            }
          }
        }

        if (!ctx || !ctx.canvas) {
          console.error('CorrelationMatrix: Context became invalid before chart creation')
          return
        }

        try {
          chart.value = new Chart(ctx, config)
          console.log('CorrelationMatrix: Chart created successfully')
        } catch (chartError) {
          console.error('CorrelationMatrix: Error creating Chart.js instance:', chartError)
          
          if (chart.value) {
            try {
              if (typeof chart.value.destroy === 'function') {
                chart.value.destroy()
              }
            } catch (destroyError) {
              console.warn('CorrelationMatrix: Error destroying chart after creation error:', destroyError)
            }
            chart.value = null
          }

          try {
            ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)
          } catch (clearError) {
            console.warn('CorrelationMatrix: Error clearing canvas after chart creation error:', clearError)
          }

          return
        }

      } catch (error) {
        console.warn('CorrelationMatrix: General error in createChart:', error)
        if (chart.value) {
          try {
            if (typeof chart.value.destroy === 'function') {
              chart.value.destroy()
            }
          } catch (destroyError) {
            console.warn('CorrelationMatrix: Error destroying chart after general error:', destroyError)
          }
          chart.value = null
        }
      }
    }

    onMounted(async () => {
      await createChart()
    })

    onUnmounted(() => {
      if (chart.value) {
        try {
          if (typeof chart.value.destroy === 'function') {
            chart.value.destroy()
          }
        } catch (e) {
          console.warn('CorrelationMatrix: Error destroying chart on unmount:', e)
        }
        chart.value = null
      }
      chartCanvas.value = null
    })

    watch(() => props.clusters, (newClusters) => {
      console.log('🔗 CorrelationMatrix received new clusters:', newClusters)
      if (newClusters && newClusters.length > 0) {
        createChart()
      }
    }, { deep: true })

    return {
      chartCanvas,
      correlationInsights,
      getCorrelationClass
    }
  }
}
</script>

<style scoped>
.correlation-matrix-container {
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

.chart-info p {
  color: #718096;
  font-size: 0.875rem;
  margin: 0;
  line-height: 1.5;
}

.chart-wrapper {
  height: 400px;
  position: relative;
}

.correlation-legend {
  margin: 1rem 0;
  padding: 1rem;
  background: #f7fafc;
  border-radius: 8px;
}

.legend-scale {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.scale-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: #4a5568;
}

.color-box {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
}

.correlation-insights {
  margin-top: 2rem;
}

.correlation-insights h4 {
  color: #2d3748;
  margin-bottom: 1rem;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.insight-card {
  background: #f7fafc;
  border-radius: 8px;
  padding: 1rem;
  border-left: 4px solid #667eea;
}

.insight-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.insight-variables {
  font-weight: 600;
  color: #2d3748;
  font-size: 0.875rem;
}

.insight-value {
  font-weight: 700;
  font-size: 1rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  color: white;
}

.correlation-very-strong { background-color: #2d3748; }
.correlation-strong { background-color: #4a5568; }
.correlation-moderate { background-color: #667eea; }
.correlation-weak { background-color: #a0aec0; }
.correlation-very-weak { background-color: #cbd5e0; color: #2d3748; }

.insight-description {
  color: #718096;
  font-size: 0.875rem;
  line-height: 1.4;
  margin: 0;
}

@media (max-width: 768px) {
  .legend-scale {
    flex-direction: column;
    align-items: stretch;
  }
  
  .scale-item {
    justify-content: center;
  }
  
  .chart-wrapper {
    height: 300px;
  }
  
  .insights-grid {
    grid-template-columns: 1fr;
  }
}
</style>