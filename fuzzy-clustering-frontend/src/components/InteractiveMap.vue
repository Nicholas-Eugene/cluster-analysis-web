<template>
  <div class="map-container">
    <div class="map-header">
      <h3>{{ title }}</h3>
      <div class="map-controls">
        <div class="cluster-filter">
          <label>Filter Cluster:</label>
          <select v-model="selectedClusterFilter" @change="updateMapView">
            <option value="all">Semua Cluster</option>
            <option v-for="cluster in clusters" :key="cluster.id" :value="cluster.id">
              Cluster {{ cluster.id }}
            </option>
          </select>
        </div>
        <div class="map-info">
          <span>{{ filteredMarkers.length }} daerah ditampilkan</span>
        </div>
      </div>
    </div>
    
    <div class="map-wrapper">
      <div id="map" ref="mapContainer"></div>
    </div>
    
    <div class="map-legend">
      <h4>Legenda Cluster</h4>
      <div class="legend-items">
        <div v-for="(cluster, index) in clusters" :key="cluster.id" class="legend-item">
          <div class="legend-marker" :style="{ backgroundColor: getClusterColor(index) }"></div>
          <span>Cluster {{ cluster.id }} ({{ cluster.size }} daerah)</span>
        </div>
      </div>
      <div class="map-stats">
        <div class="stat-item">
          <strong>Total Daerah:</strong> {{ totalRegions }}
        </div>
        <div class="stat-item">
          <strong>Daerah Terplot:</strong> {{ mappedRegions }}
        </div>
        <div class="stat-item">
          <strong>Coverage:</strong> {{ coveragePercentage }}%
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import L from 'leaflet'

// Fix for default markers in Leaflet with Vite
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

// Indonesian city coordinates - comprehensive dataset
const cityCoords = {
  // Aceh
  'Aceh Barat': [4.4531, 96.1265],
  'Aceh Barat Daya': [3.8335, 96.8417],
  'Aceh Besar': [5.3686, 95.4678],
  'Aceh Jaya': [4.8028, 95.7369],
  'Aceh Selatan': [3.2081, 97.2608],
  'Aceh Singkil': [2.4988, 97.8398],
  'Aceh Tamiang': [4.2694, 98.0194],
  'Aceh Tengah': [4.5165, 96.8417],
  'Aceh Tenggara': [3.3769, 97.7124],
  'Aceh Timur': [4.6401, 97.6256],
  'Aceh Utara': [4.9961, 97.2144],
  'Bener Meriah': [4.7479, 96.8601],
  'Bireuen': [5.0872, 96.6559],
  'Gayo Lues': [3.9789, 97.3592],
  'Nagan Raya': [4.1557, 96.5369],
  'Pidie': [5.0244, 96.0968],
  'Pidie Jaya': [5.1278, 96.2238],
  'Simeulue': [2.6052, 96.0791],
  'Banda Aceh': [5.5501, 95.3187],
  'Langsa': [4.4735, 97.9702],
  'Lhokseumawe': [5.1764, 97.1436],
  'Sabang': [5.8824, 95.3245],
  'Subulussalam': [2.7667, 97.9167],

  // Sumatera Utara
  'Asahan': [2.7699, 99.5303],
  'Batu Bara': [3.2000, 99.4167],
  'Dairi': [2.8167, 98.2500],
  'Deli Serdang': [3.5333, 98.7167],
  'Humbang Hasundutan': [2.2612, 98.5137],
  'Karo': [3.1000, 98.3000],
  'Labuhanbatu': [2.1667, 100.1667],
  'Labuhanbatu Selatan': [2.0333, 100.1333],
  'Labuhanbatu Utara': [2.5167, 99.7500],
  'Langkat': [3.7333, 98.2167],
  'Mandailing Natal': [0.7833, 99.2500],
  'Nias': [1.0833, 97.7500],
  'Nias Barat': [1.0000, 97.4167],
  'Nias Selatan': [0.5500, 97.7833],
  'Nias Utara': [1.3333, 97.3333],
  'Padang Lawas': [1.4167, 99.8333],
  'Padang Lawas Utara': [1.6667, 99.6667],
  'Pakpak Bharat': [2.5667, 98.3000],
  'Samosir': [2.6167, 98.7167],
  'Serdang Bedagai': [3.3333, 99.0000],
  'Simalungun': [2.8667, 99.0000],
  'Tapanuli Selatan': [1.5833, 99.2500],
  'Tapanuli Tengah': [1.9000, 98.6667],
  'Tapanuli Utara': [2.0000, 99.0667],
  'Toba': [2.3667, 99.2167],
  'Binjai': [3.6000, 98.4833],
  'Gunungsitoli': [1.2833, 97.6167],
  'Medan': [3.5833, 98.6667],
  'Padangsidimpuan': [1.3833, 99.2667],
  'Pematangsiantar': [2.9667, 99.0667],
  'Sibolga': [1.7333, 98.7833],
  'Tanjungbalai': [2.9667, 99.8000],
  'Tebing Tinggi': [3.3333, 99.1667],

  // Jakarta
  'Jakarta Pusat': [-6.1833, 106.8333],
  'Jakarta Utara': [-6.1333, 106.8500],
  'Jakarta Barat': [-6.1667, 106.7833],
  'Jakarta Selatan': [-6.2667, 106.8167],
  'Jakarta Timur': [-6.2333, 106.8833],
  'Kepulauan Seribu': [-5.6167, 106.5833],
  'Administrasi Kepulauan Seribu': [-5.6167, 106.5833],
  'Administrasi Jakarta Barat': [-6.1667, 106.7833],
  'Administrasi Jakarta Pusat': [-6.1833, 106.8333],
  'Administrasi Jakarta Selatan': [-6.2667, 106.8167],
  'Administrasi Jakarta Timur': [-6.2333, 106.8833],
  'Administrasi Jakarta Utara': [-6.1333, 106.8500],

  // Major cities for better coverage
  'Surabaya': [-7.2500, 112.7500],
  'Bandung': [-6.9175, 107.6191],
  'Bekasi': [-6.2409, 106.9921],
  'Semarang': [-7.0000, 110.4167],
  'Makassar': [-5.1333, 119.4167],
  'Palembang': [-2.9833, 104.7667],
  'Batam': [1.0500, 104.0000],
  'Pekanbaru': [0.5333, 101.4500],
  'Bandar Lampung': [-5.4333, 105.2667],
  'Padang': [-0.9500, 100.3500],
  'Malang': [-7.9833, 112.6167],
  'Yogyakarta': [-7.8000, 110.3667],
  'Denpasar': [-8.6500, 115.2167],
  'Samarinda': [-0.5000, 117.1500],
  'Banjarmasin': [-3.3167, 114.5833],
  'Pontianak': [-0.0167, 109.3333],
  'Manado': [1.4833, 124.8500],
  'Balikpapan': [-1.2500, 116.8333],
  'Jambi': [-1.6000, 103.6167],
  'Bengkulu': [-3.8000, 102.2667],
  'Palu': [-0.8833, 119.8667],
  'Kendari': [-3.9833, 122.5167],
  'Kupang': [-10.1667, 123.5833],
  'Mataram': [-8.5833, 116.1167],
  'Ambon': [-3.7000, 128.1667],
  'Jayapura': [-2.5333, 140.7167],

  // Add more comprehensive coverage from your JSON
  'Bogor': [-6.5944, 106.7896],
  'Depok': [-6.4025, 106.7942],
  'Tangerang': [-6.1667, 106.6333],
  'Tangerang Selatan': [-6.2833, 106.7167],
  'Cirebon': [-6.7263, 108.5522],
  'Tasikmalaya': [-7.3274, 108.2206],
  'Sukabumi': [-6.9285, 106.9287],
  'Serang': [-6.1167, 106.1500],
  'Cilegon': [-6.0167, 106.0500],
  'Magelang': [-7.4833, 110.2167],
  'Surakarta': [-7.5667, 110.8167],
  'Salatiga': [-7.3333, 110.5000],
  'Tegal': [-6.8667, 109.1333],
  'Pekalongan': [-6.8833, 109.6667],
  'Kediri': [-7.8167, 112.0167],
  'Blitar': [-8.1000, 112.1667],
  'Madiun': [-7.6333, 111.5167],
  'Mojokerto': [-7.4667, 112.4333],
  'Pasuruan': [-7.6500, 112.9000],
  'Probolinggo': [-7.7500, 113.2167],
  'Batu': [-7.8833, 112.5333],

  // Add missing cities from sample data
  'Banjarmasin': [-3.3167, 114.5833],
  'Pontianak': [-0.0167, 109.3333],
  'Samarinda': [-0.5000, 117.1500],
  'Balikpapan': [-1.2500, 116.8333],
  'Manado': [1.4833, 124.8500],
  'Palu': [-0.8833, 119.8667],
  'Kendari': [-3.9833, 122.5167],
  'Jayapura': [-2.5333, 140.7167],
  'Sorong': [-0.8833, 131.2500],
  'Ambon': [-3.7000, 128.1667],
  'Kupang': [-10.1667, 123.5833],
  'Ternate': [0.7833, 127.3833],
  
  // Add more from your comprehensive list
  'Palangka Raya': [-2.2167, 113.9167],
  'Tarakan': [3.3000, 117.6333],
  'Bau-Bau': [-5.4667, 122.6000],
  'Tual': [-5.6333, 132.7500],
  'Ternate': [0.7833, 127.3833],
  'Gorontalo': [0.5333, 123.0667],
  'Mamuju': [-2.6667, 118.8833],
  'Nabire': [-3.3667, 135.5000],
  'Merauke': [-8.4833, 140.3333],
}

export default {
  name: 'InteractiveMap',
  props: {
    clusters: {
      type: Array,
      required: true
    },
    title: {
      type: String,
      default: 'Peta Sebaran Cluster'
    }
  },
  setup(props) {
    const mapContainer = ref(null)
    const map = ref(null)
    const markersLayer = ref(null)
    const selectedClusterFilter = ref('all')

    const colors = [
      '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
      '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
    ]

    const getClusterColor = (index) => {
      return colors[index % colors.length]
    }

    // Helper function to normalize city names for coordinate lookup
    const normalizeCityName = (cityName) => {
      if (!cityName) return ''
      
      // Convert to string and clean up
      let normalized = String(cityName).trim()
      
      // Handle common variations
      const replacements = {
        'Kab. ': '',
        'Kabupaten ': '',
        'Kota ': '',
        'Administrasi ': '',
        'DKI ': '',
      }
      
      for (const [key, value] of Object.entries(replacements)) {
        normalized = normalized.replace(new RegExp(key, 'gi'), value)
      }
      
      return normalized.trim()
    }

    // Get coordinates for a city
    const getCityCoordinates = (cityName) => {
      const normalized = normalizeCityName(cityName)
      
      // Direct lookup
      if (cityCoords[normalized]) {
        console.log(`✅ Found exact match for: ${cityName} -> ${normalized}`)
        return cityCoords[normalized]
      }
      
      // Fuzzy matching - try to find partial matches
      const cityKeys = Object.keys(cityCoords)
      
      // Try different matching strategies
      let fuzzyMatch = null
      
      // Strategy 1: Exact substring match
      fuzzyMatch = cityKeys.find(key => 
        key.toLowerCase().includes(normalized.toLowerCase()) ||
        normalized.toLowerCase().includes(key.toLowerCase())
      )
      
      if (fuzzyMatch) {
        console.log(`✅ Found fuzzy match for: ${cityName} -> ${fuzzyMatch}`)
        return cityCoords[fuzzyMatch]
      }
      
      // Strategy 2: Remove common words and try again
      const cleanNormalized = normalized
        .replace(/\b(kota|kabupaten|kab|administrasi)\b/gi, '')
        .trim()
      
      fuzzyMatch = cityKeys.find(key => {
        const cleanKey = key
          .replace(/\b(kota|kabupaten|kab|administrasi)\b/gi, '')
          .trim()
        return cleanKey.toLowerCase() === cleanNormalized.toLowerCase()
      })
      
      if (fuzzyMatch) {
        console.log(`✅ Found clean match for: ${cityName} -> ${fuzzyMatch}`)
        return cityCoords[fuzzyMatch]
      }
      
      // Strategy 3: Use fallback coordinates based on region
      const fallbackCoords = getFallbackCoordinates(normalized)
      if (fallbackCoords) {
        console.log(`⚠️ Using fallback coordinates for: ${cityName}`)
        return fallbackCoords
      }
      
      // Log missing coordinates for debugging
      console.warn(`❌ Coordinates not found for: "${cityName}" (normalized: "${normalized}")`)
      return null
    }
    
    // Get fallback coordinates based on province or region
    const getFallbackCoordinates = (cityName) => {
      const fallbacks = {
        // Jakarta area
        'jakarta': [-6.2, 106.8],
        // Java
        'bandung': [-6.9, 107.6],
        'surabaya': [-7.25, 112.75],
        'semarang': [-7.0, 110.4],
        'yogyakarta': [-7.8, 110.4],
        // Sumatra
        'medan': [3.58, 98.67],
        'palembang': [-2.98, 104.77],
        'padang': [-0.95, 100.35],
        'pekanbaru': [0.53, 101.45],
        'bandar lampung': [-5.43, 105.27],
        // Kalimantan
        'pontianak': [-0.02, 109.33],
        'banjarmasin': [-3.32, 114.58],
        'samarinda': [-0.5, 117.15],
        'balikpapan': [-1.25, 116.83],
        // Sulawesi
        'makassar': [-5.13, 119.42],
        'manado': [1.48, 124.85],
        'palu': [-0.88, 119.87],
        'kendari': [-3.98, 122.52],
        // Eastern Indonesia
        'denpasar': [-8.65, 115.22],
        'mataram': [-8.58, 116.12],
        'kupang': [-10.17, 123.58],
        'ambon': [-3.7, 128.17],
        'jayapura': [-2.53, 140.72],
      }
      
      const cityLower = cityName.toLowerCase()
      for (const [key, coords] of Object.entries(fallbacks)) {
        if (cityLower.includes(key) || key.includes(cityLower)) {
          return coords
        }
      }
      
      return null
    }

    const filteredMarkers = computed(() => {
      let allMarkers = []
      
      props.clusters.forEach((cluster, clusterIndex) => {
        if (selectedClusterFilter.value !== 'all' && cluster.id !== selectedClusterFilter.value) {
          return
        }
        
        cluster.members.forEach(member => {
          const coords = getCityCoordinates(member.kabupaten_kota)
          if (coords) {
            allMarkers.push({
              ...member,
              cluster: cluster,
              clusterIndex: clusterIndex,
              coordinates: coords
            })
          }
        })
      })
      
      return allMarkers
    })

    const totalRegions = computed(() => {
      return props.clusters.reduce((total, cluster) => total + cluster.size, 0)
    })

    const mappedRegions = computed(() => {
      return filteredMarkers.value.length
    })

    const coveragePercentage = computed(() => {
      if (totalRegions.value === 0) return 0
      return Math.round((mappedRegions.value / totalRegions.value) * 100)
    })

    const initMap = () => {
      if (!mapContainer.value) return

      // Initialize map centered on Indonesia
      map.value = L.map(mapContainer.value).setView([-2.5, 118], 5)

      // Add OpenStreetMap tiles with better styling
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18
      }).addTo(map.value)

      // Initialize markers layer
      markersLayer.value = L.layerGroup().addTo(map.value)

      // Load initial markers
      updateMapView()
    }

    const updateMapView = () => {
      if (!map.value || !markersLayer.value) return

      // Clear existing markers
      markersLayer.value.clearLayers()

      console.log(`🗺️ Updating map with ${filteredMarkers.value.length} markers`)
      console.log('📊 Clusters data:', props.clusters)
      console.log('🎯 Filtered markers:', filteredMarkers.value.slice(0, 3)) // Show first 3 for debugging

      // Add markers for filtered data
      filteredMarkers.value.forEach((markerData, index) => {
        const { coordinates, cluster, clusterIndex } = markerData
        const color = getClusterColor(clusterIndex)
        
        console.log(`📍 Creating marker ${index + 1}: ${markerData.kabupaten_kota} at [${coordinates[0]}, ${coordinates[1]}] - Cluster ${cluster.id}`)
        
        const marker = L.circleMarker(coordinates, {
          radius: 10,
          fillColor: color,
          color: '#fff',
          weight: 3,
          opacity: 1,
          fillOpacity: 0.9
        })

        // Create popup content with better formatting
        const popupContent = `
          <div class="marker-popup">
            <h4>${markerData.kabupaten_kota}</h4>
            <div class="popup-cluster">
              <span class="cluster-badge" style="background-color: ${color}">
                Cluster ${cluster.id}
              </span>
            </div>
            <div class="popup-stats">
              <div class="stat-row">
                <span class="stat-label">IPM:</span>
                <span class="stat-value">${markerData.ipm?.toFixed(2) || 'N/A'}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">Garis Kemiskinan:</span>
                <span class="stat-value">Rp ${markerData.garis_kemiskinan?.toLocaleString('id-ID') || 'N/A'}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">Pengeluaran per Kapita:</span>
                <span class="stat-value">Rp ${markerData.pengeluaran_per_kapita?.toLocaleString('id-ID') || 'N/A'}</span>
              </div>
              ${markerData.membership ? `
                <div class="stat-row">
                  <span class="stat-label">Membership:</span>
                  <span class="stat-value">${(markerData.membership * 100).toFixed(1)}%</span>
                </div>
              ` : ''}
              ${markerData.tahun ? `
                <div class="stat-row">
                  <span class="stat-label">Tahun:</span>
                  <span class="stat-value">${markerData.tahun}</span>
                </div>
              ` : ''}
            </div>
          </div>
        `

        marker.bindPopup(popupContent, {
          maxWidth: 300,
          className: 'custom-popup'
        })
        
        markersLayer.value.addLayer(marker)
      })

      // Auto-fit map bounds if there are markers
      if (filteredMarkers.value.length > 0) {
        const group = new L.featureGroup(markersLayer.value.getLayers())
        map.value.fitBounds(group.getBounds().pad(0.1))
      }
    }

    onMounted(() => {
      initMap()
    })

    onUnmounted(() => {
      if (map.value) {
        map.value.remove()
      }
    })

    watch(() => props.clusters, () => {
      updateMapView()
    }, { deep: true })

    return {
      mapContainer,
      selectedClusterFilter,
      filteredMarkers,
      totalRegions,
      mappedRegions,
      coveragePercentage,
      getClusterColor,
      updateMapView
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
  flex-wrap: wrap;
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

.map-info {
  background: #f7fafc;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #4a5568;
  border: 1px solid #e2e8f0;
}

.map-wrapper {
  height: 500px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  position: relative;
}

#map {
  height: 100%;
  width: 100%;
}

.map-legend {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.map-legend h4 {
  color: #2d3748;
  margin: 0 0 1rem 0;
  font-size: 1rem;
}

.legend-items {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #4a5568;
}

.legend-marker {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.1);
}

.map-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.stat-item {
  background: #f7fafc;
  padding: 0.75rem;
  border-radius: 6px;
  text-align: center;
  font-size: 0.875rem;
}

.stat-item strong {
  color: #2d3748;
  display: block;
  margin-bottom: 0.25rem;
}

@media (max-width: 768px) {
  .map-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .map-controls {
    justify-content: center;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .map-wrapper {
    height: 400px;
  }
  
  .legend-items {
    justify-content: center;
  }
  
  .map-stats {
    grid-template-columns: 1fr;
  }
}

/* Custom popup styles */
:global(.custom-popup .leaflet-popup-content) {
  margin: 0;
  padding: 0;
}

:global(.marker-popup) {
  min-width: 250px;
}

:global(.marker-popup h4) {
  margin: 0 0 0.5rem 0;
  color: #2d3748;
  font-size: 1rem;
  font-weight: 600;
}

:global(.popup-cluster) {
  margin-bottom: 0.75rem;
}

:global(.cluster-badge) {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

:global(.popup-stats) {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

:global(.stat-row) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.25rem 0;
  border-bottom: 1px solid #f1f5f9;
}

:global(.stat-row:last-child) {
  border-bottom: none;
}

:global(.stat-label) {
  font-weight: 500;
  color: #64748b;
  font-size: 0.875rem;
}

:global(.stat-value) {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.875rem;
}
</style>