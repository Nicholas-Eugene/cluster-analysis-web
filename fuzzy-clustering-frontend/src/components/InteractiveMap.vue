<template>
  <div class="map-container">
    <div class="map-header">
      <h3>{{ title }}</h3>
      <div class="map-controls">
        <select v-model="selectedMetric" @change="updateMapColors" class="metric-select">
          <option value="cluster">Cluster</option>
          <option value="ipm">IPM</option>
          <option value="garis_kemiskinan">Garis Kemiskinan</option>
          <option value="pengeluaran_per_kapita">Pengeluaran Per Kapita</option>
        </select>
        <button @click="fitMapToBounds" class="btn btn-sm">
          🎯 Fit to Indonesia
        </button>
      </div>
    </div>
    <div class="map-wrapper">
      <div ref="mapContainer" class="map"></div>
    </div>
    <div class="map-legend">
      <div v-if="selectedMetric === 'cluster'" class="cluster-legend">
        <div v-for="(cluster, index) in clusters" :key="cluster.id" class="legend-item">
          <div class="legend-color" :style="{ backgroundColor: getClusterColor(index) }"></div>
          <span>Cluster {{ cluster.id }} ({{ cluster.size }} daerah)</span>
        </div>
      </div>
      <div v-else class="metric-legend">
        <div class="legend-gradient">
          <div class="gradient-bar" :style="{ background: getGradientStyle() }"></div>
          <div class="gradient-labels">
            <span>{{ formatValue(metricRange.min) }}</span>
            <span>{{ formatValue(metricRange.max) }}</span>
          </div>
        </div>
        <div class="legend-title">{{ getMetricLabel(selectedMetric) }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix for default markers in Leaflet
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

export default {
  name: 'InteractiveMap',
  props: {
    clusters: {
      type: Array,
      required: true
    },
    title: {
      type: String,
      default: 'Peta Interaktif Clustering'
    }
  },
  setup(props) {
    const mapContainer = ref(null)
    const map = ref(null)
    const markers = ref([])
    const selectedMetric = ref('cluster')

    const colors = [
      '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
      '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
    ]

    const getClusterColor = (index) => {
      return colors[index % colors.length]
    }

    const allMembers = computed(() => {
      return props.clusters.flatMap((cluster, clusterIndex) => 
        cluster.members.map(member => ({
          ...member,
          clusterIndex,
          clusterId: cluster.id
        }))
      )
    })

    const metricRange = computed(() => {
      if (selectedMetric.value === 'cluster') return { min: 0, max: props.clusters.length }
      
      const values = allMembers.value
        .map(member => member[selectedMetric.value])
        .filter(val => val != null && !isNaN(val))
      
      return {
        min: Math.min(...values),
        max: Math.max(...values)
      }
    })

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

    const getMetricLabel = (metric) => {
      const labels = {
        'cluster': 'Cluster',
        'ipm': 'IPM',
        'garis_kemiskinan': 'Garis Kemiskinan',
        'pengeluaran_per_kapita': 'Pengeluaran Per Kapita'
      }
      return labels[metric] || metric
    }

    const getGradientStyle = () => {
      if (selectedMetric.value === 'cluster') return ''
      return 'linear-gradient(to right, #3182ce, #63b3ed, #90cdf4, #bee3f8)'
    }

    const getMarkerColor = (member) => {
      if (selectedMetric.value === 'cluster') {
        return getClusterColor(member.clusterIndex)
      }
      
      // Color based on metric value
      const value = member[selectedMetric.value]
      const range = metricRange.value
      const normalized = (value - range.min) / (range.max - range.min)
      
      // Create color gradient from blue to red
      const hue = (1 - normalized) * 240 // 240 = blue, 0 = red
      return `hsl(${hue}, 70%, 50%)`
    }

    const createCustomIcon = (color, size = 'medium') => {
      const sizes = {
        small: [20, 20],
        medium: [25, 25],
        large: [30, 30]
      }
      
      const [width, height] = sizes[size] || sizes.medium
      
      return L.divIcon({
        className: 'custom-marker',
        html: `<div style="
          background-color: ${color};
          width: ${width}px;
          height: ${height}px;
          border-radius: 50%;
          border: 3px solid white;
          box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        "></div>`,
        iconSize: [width, height],
        iconAnchor: [width/2, height/2]
      })
    }

    const createPopupContent = (member) => {
      const membershipText = member.membership && member.membership < 1.0 
        ? `<br><strong>Membership:</strong> ${(member.membership * 100).toFixed(1)}%`
        : ''
      
      return `
        <div class="map-popup">
          <h4>${member.kabupaten_kota}</h4>
          <p><strong>Provinsi:</strong> ${member.provinsi || 'N/A'}</p>
          <p><strong>Tahun:</strong> ${member.tahun}</p>
          <p><strong>Cluster:</strong> ${member.clusterId}</p>
          <hr>
          <p><strong>IPM:</strong> ${member.ipm?.toFixed(2) || 'N/A'}</p>
          <p><strong>Garis Kemiskinan:</strong> ${formatValue(member.garis_kemiskinan || 0)}</p>
          <p><strong>Pengeluaran Per Kapita:</strong> ${formatValue(member.pengeluaran_per_kapita || 0)}</p>
          ${membershipText}
        </div>
      `
    }

    const initializeMap = () => {
      if (!mapContainer.value) return

      // Initialize map centered on Indonesia
      map.value = L.map(mapContainer.value).setView([-2.5, 118], 5)

      // Add tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(map.value)

      // Add markers
      updateMarkers()
    }

    const updateMarkers = () => {
      if (!map.value) return

      // Clear existing markers
      markers.value.forEach(marker => map.value.removeLayer(marker))
      markers.value = []

      // Add new markers
      allMembers.value.forEach(member => {
        if (member.latitude && member.longitude) {
          const color = getMarkerColor(member)
          const size = member.membership ? 
            (member.membership > 0.7 ? 'large' : member.membership > 0.4 ? 'medium' : 'small') : 
            'medium'
          
          const marker = L.marker([member.latitude, member.longitude], {
            icon: createCustomIcon(color, size)
          })
          .bindPopup(createPopupContent(member))
          .addTo(map.value)

          markers.value.push(marker)
        }
      })
    }

    const updateMapColors = () => {
      updateMarkers()
    }

    const fitMapToBounds = () => {
      if (!map.value || markers.value.length === 0) return

      const group = new L.featureGroup(markers.value)
      map.value.fitBounds(group.getBounds().pad(0.1))
    }

    onMounted(() => {
      initializeMap()
    })

    onUnmounted(() => {
      if (map.value) {
        map.value.remove()
      }
    })

    watch(() => props.clusters, () => {
      updateMarkers()
    }, { deep: true })

    return {
      mapContainer,
      selectedMetric,
      metricRange,
      getClusterColor,
      formatValue,
      getMetricLabel,
      getGradientStyle,
      updateMapColors,
      fitMapToBounds
    }
  }
}
</script>

<style scoped>
.map-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.map-header h3 {
  color: #2d3748;
  margin: 0;
  font-size: 1.25rem;
}

.map-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.metric-select {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: white;
  color: #4a5568;
  font-size: 0.875rem;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-sm:hover {
  background: #5a67d8;
}

.map-wrapper {
  height: 500px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.map {
  height: 100%;
  width: 100%;
}

.map-legend {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.cluster-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
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

.metric-legend {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.legend-gradient {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.gradient-bar {
  width: 200px;
  height: 20px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.gradient-labels {
  display: flex;
  justify-content: space-between;
  width: 200px;
  font-size: 0.75rem;
  color: #718096;
}

.legend-title {
  font-size: 0.875rem;
  color: #4a5568;
  font-weight: 600;
}

/* Custom popup styles */
:deep(.map-popup) {
  font-family: inherit;
}

:deep(.map-popup h4) {
  color: #2d3748;
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

:deep(.map-popup p) {
  margin: 0.25rem 0;
  font-size: 0.875rem;
  color: #4a5568;
}

:deep(.map-popup hr) {
  border: none;
  border-top: 1px solid #e2e8f0;
  margin: 0.5rem 0;
}

@media (max-width: 768px) {
  .map-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .map-controls {
    justify-content: center;
  }
  
  .map-wrapper {
    height: 400px;
  }
  
  .cluster-legend {
    justify-content: center;
  }
  
  .gradient-bar,
  .gradient-labels {
    width: 150px;
  }
}
</style>