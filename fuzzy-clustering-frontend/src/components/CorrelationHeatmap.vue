<template>
  <div class="heatmap-container">
    <div class="heatmap-header">
      <h3>{{ title }}</h3>
      <div class="heatmap-controls">
        <div class="cluster-filter">
          <label>Filter Cluster:</label>
          <select v-model="selectedCluster" @change="updateHeatmap">
            <option value="all">Semua Cluster</option>
            <option v-for="cluster in clusters" :key="cluster.id" :value="cluster.id">
              {{ cluster.interpretation?.label || `Cluster ${cluster.id}` }}
            </option>
          </select>
        </div>
      </div>
    </div>
    
    <div class="heatmap-wrapper">
      <canvas ref="heatmapCanvas" class="heatmap-canvas"></canvas>
    </div>
    
    <div class="heatmap-legend">
      <div class="correlation-scale">
        <div class="scale-bar">
          <div class="scale-gradient"></div>
        </div>
        <div class="scale-labels">
          <span>-1.0</span>
          <span>-0.5</span>
          <span>0.0</span>
          <span>0.5</span>
          <span>1.0</span>
        </div>
        <div class="scale-title">Koefisien Korelasi</div>
      </div>
      <div class="heatmap-info">
        <div class="info-item">
          <strong>Data Points:</strong> {{ dataPointsCount }}
        </div>
        <div class="info-item">
          <strong>Variables:</strong> IPM, Garis Kemiskinan, Pengeluaran per Kapita
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'

export default {
  name: 'CorrelationHeatmap',
  props: {
    clusters: {
      type: Array,
      required: true
    },
    title: {
      type: String,
      default: 'Heatmap Korelasi Antar Variabel'
    }
  },
  setup(props) {
    const heatmapCanvas = ref(null)
    const selectedCluster = ref('all')
    
    const variables = ['IPM', 'Garis Kemiskinan', 'Pengeluaran per Kapita']
    const variableKeys = ['ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita']
    
    // Get filtered data based on selected cluster
    const filteredData = computed(() => {
      let allData = []
      
      props.clusters.forEach(cluster => {
        if (selectedCluster.value === 'all' || cluster.id === selectedCluster.value) {
          cluster.members.forEach(member => {
            if (member.ipm && member.garis_kemiskinan && member.pengeluaran_per_kapita) {
              allData.push({
                ipm: member.ipm,
                garis_kemiskinan: member.garis_kemiskinan,
                pengeluaran_per_kapita: member.pengeluaran_per_kapita
              })
            }
          })
        }
      })
      
      return allData
    })
    
    const dataPointsCount = computed(() => filteredData.value.length)
    
    // Calculate correlation matrix
    const calculateCorrelation = (data) => {
      const n = data.length
      if (n < 2) return null
      
      const correlationMatrix = []
      
      for (let i = 0; i < variableKeys.length; i++) {
        correlationMatrix[i] = []
        for (let j = 0; j < variableKeys.length; j++) {
          if (i === j) {
            correlationMatrix[i][j] = 1.0
          } else {
            const x = data.map(d => d[variableKeys[i]])
            const y = data.map(d => d[variableKeys[j]])
            correlationMatrix[i][j] = pearsonCorrelation(x, y)
          }
        }
      }
      
      return correlationMatrix
    }
    
    // Calculate Pearson correlation coefficient
    const pearsonCorrelation = (x, y) => {
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
    
    // Import color utility from design system
    const getCorrelationColor = (correlation) => {
      const absCorr = Math.abs(correlation)
      
      if (correlation > 0) {
        // Positive correlation: white to purple (matching UI theme)
        const r = 102 + (255 - 102) * (1 - absCorr * 0.9)
        const g = 126 + (255 - 126) * (1 - absCorr * 0.9)
        const b = 234 + (255 - 234) * (1 - absCorr * 0.9)
        return `rgba(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)}, 1)`
      } else if (correlation < 0) {
        // Negative correlation: white to green (matching success color)
        const r = 72 + (255 - 72) * (1 - absCorr * 0.9)
        const g = 187 + (255 - 187) * (1 - absCorr * 0.9)
        const b = 120 + (255 - 120) * (1 - absCorr * 0.9)
        return `rgba(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)}, 1)`
      } else {
        // No correlation: white
        return 'rgba(255, 255, 255, 1)'
      }
    }
    
    // Draw heatmap
    const drawHeatmap = () => {
      if (!heatmapCanvas.value) return
      
      const canvas = heatmapCanvas.value
      const ctx = canvas.getContext('2d')
      
      const containerWidth = canvas.parentElement.clientWidth
      const margin = {
        top: 180,
        right: 80,
        bottom: 20,
        left: 220
      }
      
      const size = Math.min(containerWidth - 40, 400)
      const totalWidth = size + margin.left + margin.right
      const totalHeight = size + margin.top + margin.bottom
      
      canvas.width = totalWidth
      canvas.height = totalHeight
      canvas.style.width = totalWidth + 'px'
      canvas.style.height = totalHeight + 'px'
      
      // Clear canvas
      ctx.clearRect(0, 0, size, size)
      
      const data = filteredData.value
      if (data.length === 0) {
        // Draw "No data" message
        ctx.fillStyle = '#666'
        ctx.font = '16px Arial'
        ctx.textAlign = 'center'
        ctx.fillText('No data available', size / 2, size / 2)
        return
      }
      
      const correlationMatrix = calculateCorrelation(data)
      if (!correlationMatrix) return
      
      const cellSize = size / variables.length
      const padding = 2
      
      // Draw heatmap cells
      for (let i = 0; i < variables.length; i++) {
        for (let j = 0; j < variables.length; j++) {
          const x = margin.left + j * cellSize + padding
          const y = margin.top + i * cellSize + padding
          const width = cellSize - 2 * padding
          const height = cellSize - 2 * padding
          
          const correlation = correlationMatrix[i][j]
          const color = getCorrelationColor(correlation)
          
          // Draw cell background
          ctx.fillStyle = color
          ctx.fillRect(x, y, width, height)
          
          // Draw cell border
          ctx.strokeStyle = '#e2e8f0'
          ctx.lineWidth = 1
          ctx.strokeRect(x, y, width, height)
          
          // Draw correlation value
          ctx.fillStyle = Math.abs(correlation) > 0.5 ? 'white' : 'black'
          ctx.font = 'bold 14px Arial'
          ctx.textAlign = 'center'
          ctx.textBaseline = 'middle'
          ctx.fillText(
            correlation.toFixed(2),
            x + width / 2,
            y + height / 2
          )
        }
      }
      
      // Draw variable labels
      ctx.fillStyle = '#2d3748'
      ctx.font = 'bold 16px Arial' // Increased font size
      
      // Top labels
      for (let j = 0; j < variables.length; j++) {
        const x = margin.left + j * cellSize + cellSize / 2
        const y = margin.top - 30 // Increased distance from heatmap
        ctx.save()
        ctx.textAlign = 'left'
        ctx.textBaseline = 'middle'
        ctx.translate(x, y)
        ctx.rotate(-Math.PI / 4)
        // Add background for better readability
        const textWidth = ctx.measureText(variables[j]).width
        ctx.fillStyle = 'rgba(255, 255, 255, 0.9)'
        ctx.fillRect(-2, -10, textWidth + 4, 20)
        // Draw text
        ctx.fillStyle = '#2d3748'
        ctx.fillText(variables[j], 0, 0)
        ctx.restore()
      }
      
      // Left labels
      ctx.textAlign = 'right'
      ctx.textBaseline = 'middle'
      for (let i = 0; i < variables.length; i++) {
        const x = margin.left - 25 // Increased distance from heatmap
        const y = margin.top + i * cellSize + cellSize / 2
        // Add background for better readability
        const textWidth = ctx.measureText(variables[i]).width
        ctx.fillStyle = 'rgba(255, 255, 255, 0.9)'
        ctx.fillRect(x - textWidth - 2, y - 10, textWidth + 4, 20)
        // Draw text
        ctx.fillStyle = '#2d3748'
        ctx.fillText(variables[i], x, y)
      }
      
      // Draw axis lines
      ctx.strokeStyle = '#e2e8f0'
      ctx.lineWidth = 2
      // Vertical axis
      ctx.beginPath()
      ctx.moveTo(margin.left - 5, margin.top - 5)
      ctx.lineTo(margin.left - 5, margin.top + size + 5)
      ctx.stroke()
      // Horizontal axis
      ctx.beginPath()
      ctx.moveTo(margin.left - 5, margin.top - 5)
      ctx.lineTo(margin.left + size + 5, margin.top - 5)
      ctx.stroke()
    }
    
    const updateHeatmap = () => {
      setTimeout(() => {
        drawHeatmap()
      }, 100)
    }
    
    onMounted(() => {
      updateHeatmap()
      window.addEventListener('resize', updateHeatmap)
    })
    
    onUnmounted(() => {
      window.removeEventListener('resize', updateHeatmap)
    })
    
    watch(() => props.clusters, () => {
      updateHeatmap()
    }, { deep: true })
    
    watch(() => selectedCluster.value, () => {
      updateHeatmap()
    })
    
    return {
      heatmapCanvas,
      selectedCluster,
      dataPointsCount,
      updateHeatmap
    }
  }
}
</script>

<style scoped>
.heatmap-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.heatmap-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.heatmap-header h3 {
  color: #2d3748;
  margin: 0;
  font-size: 1.25rem;
}

.heatmap-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.cluster-filter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cluster-filter label {
  font-weight: 600;
  color: #4a5568;
  font-size: 0.875rem;
}

.cluster-filter select {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: white;
  color: #4a5568;
  font-size: 0.875rem;
  min-width: 150px;
}

.heatmap-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  padding: 2rem 0;
}

.heatmap-canvas {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.heatmap-legend {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.correlation-scale {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.scale-bar {
  width: 300px;
  height: 20px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  overflow: hidden;
}

.scale-gradient {
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, 
    rgba(72, 187, 120, 1) 0%,
    rgba(72, 187, 120, 0.5) 25%,
    rgba(255, 255, 255, 1) 50%,
    rgba(102, 126, 234, 0.5) 75%,
    rgba(102, 126, 234, 1) 100%
  );
}

.scale-labels {
  display: flex;
  justify-content: space-between;
  width: 300px;
  font-size: 0.75rem;
  color: #718096;
}

.scale-title {
  font-size: 0.875rem;
  color: #4a5568;
  font-weight: 600;
}

.heatmap-info {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.info-item {
  background: #f7fafc;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
  text-align: center;
}

.info-item strong {
  color: #2d3748;
  display: block;
  margin-bottom: 0.25rem;
}

@media (max-width: 768px) {
  .heatmap-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .heatmap-controls {
    justify-content: center;
  }
  
  .scale-bar,
  .scale-labels {
    width: 250px;
  }
  
  .heatmap-info {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>