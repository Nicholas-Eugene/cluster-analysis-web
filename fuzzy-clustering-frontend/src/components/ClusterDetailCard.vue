<template>
  <div class="cluster-detail-card card">
    <h3>🔍 Detail Cluster</h3>
    <div class="cluster-tabs">
      <button 
        v-for="(cluster, index) in clusters" 
        :key="`cluster-${index}`"
        @click="selectCluster(cluster.id)"
        :class="['cluster-tab', { active: isClusterActive(cluster.id) }]"
        :style="{ borderColor: getClusterColor(index) }"
      >
        <div class="tab-color" :style="{ backgroundColor: getClusterColor(index) }"></div>
        {{ cluster.interpretation?.label || `Cluster ${cluster.id}` }} ({{ cluster.size }})
      </button>
    </div>
    
    <div v-if="activeCluster" class="cluster-detail">
      <div class="cluster-info">
        <h4>{{ getClusterLabel(activeCluster) }}</h4>
        <div class="cluster-stats">
          <div class="stat-item">
            <span class="stat-label">Jumlah Daerah:</span>
            <span class="stat-value">{{ activeCluster.size }}</span>
          </div>
          <div v-if="activeCluster.centroid" class="centroid-info">
            <h5>Centroid (Rata-rata Cluster):</h5>
            <div class="centroid-values">
              <div class="centroid-item">
                <span>IPM:</span>
                <span>{{ activeCluster.centroid.ipm?.toFixed(2) || 'N/A' }}</span>
              </div>
              <div class="centroid-item">
                <span>Garis Kemiskinan:</span>
                <span>{{ formatCurrency(activeCluster.centroid.garis_kemiskinan) }} / bulan</span>
              </div>
              <div class="centroid-item">
                <span>Pengeluaran Per Kapita:</span>
                <span>{{ formatCurrency(activeCluster.centroid.pengeluaran_per_kapita * 1000) }} /tahun</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="cluster-members">
        <div class="members-header">
          <h5>Daftar Daerah ({{ filteredMembers.length }} dari {{ activeCluster.members.length }}):</h5>
          <div class="members-controls">
            <div class="search-box">
              <span class="search-icon">🔍</span>
              <input 
                v-model="searchQuery" 
                type="text" 
                placeholder="Cari daerah..." 
                class="search-input"
              />
              <button 
                v-if="searchQuery" 
                @click="searchQuery = ''" 
                class="clear-search"
                title="Hapus pencarian"
              >
                ✕
              </button>
            </div>
            <div class="sort-box">
              <label for="sort-select">Urutkan:</label>
              <select v-model="sortBy" id="sort-select" class="sort-select">
                <option value="name-asc">Nama (A-Z)</option>
                <option value="name-desc">Nama (Z-A)</option>
                <option value="ipm-asc">IPM (Terendah)</option>
                <option value="ipm-desc">IPM (Tertinggi)</option>
                <option value="poverty-asc">Kemiskinan (Terendah)</option>
                <option value="poverty-desc">Kemiskinan (Tertinggi)</option>
                <option value="expenditure-asc">Pengeluaran (Terendah)</option>
                <option value="expenditure-desc">Pengeluaran (Tertinggi)</option>
                <option v-if="showMembership" value="membership-desc">Membership (Tertinggi)</option>
                <option v-if="showMembership" value="membership-asc">Membership (Terendah)</option>
              </select>
            </div>
          </div>
        </div>
        
        <div v-if="filteredMembers.length === 0" class="no-results">
          <p>🔍 Tidak ada daerah yang cocok dengan pencarian "{{ searchQuery }}"</p>
        </div>
        
        <div v-else class="members-grid">
          <div 
            v-for="member in filteredMembers" 
            :key="`${member.kabupaten_kota}-${member.tahun || 'all'}`"
            class="member-card"
          >
            <h6>{{ member.kabupaten_kota }}</h6>
            <p v-if="member.provinsi" class="member-province">{{ member.provinsi }}</p>
            <div class="member-stats">
              <div class="member-stat">
                <span>IPM:</span>
                <span>{{ member.ipm?.toFixed(2) || 'N/A' }}</span>
              </div>
              <div class="member-stat">
                <span>Garis Kemiskinan:</span>
                <span>{{ formatCurrency(member.garis_kemiskinan) }} / bulan</span>
              </div>
              <div class="member-stat">
                <span>Pengeluaran:</span>
                <span>{{ formatCurrency(member.pengeluaran_per_kapita * 1000)}} / tahun</span>
              </div>
              <div v-if="showMembership && member.membership != null" class="member-stat membership-stat">
                <span>Membership:</span>
                <div class="membership-bar-mini">
                  <div 
                    class="membership-fill-mini" 
                    :style="{ 
                      width: `${member.membership * 100}%`,
                      backgroundColor: getClusterColor(clusters.findIndex(c => normalizeId(c.id) === normalizeId(activeCluster.id)))
                    }"
                  ></div>
                  <span class="membership-text-mini">{{ (member.membership * 100).toFixed(1) }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'

export default {
  name: 'ClusterDetailCard',
  props: {
    clusters: {
      type: Array,
      required: true
    },
    showMembership: {
      type: Boolean,
      default: true
    }
  },
  setup(props) {
    const selectedClusterId = ref(null)
    const searchQuery = ref('')
    const sortBy = ref('name-asc')

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

    // Helper to normalize cluster ID (convert to number if possible, handle 0 and -1 properly)
    const normalizeId = (id) => {
      // Explicitly handle null/undefined
      if (id === null || id === undefined) return null
      
      // Try to convert to number
      const num = Number(id)
      
      // Return number if it's valid (including 0 and -1!), otherwise return original
      return isNaN(num) ? id : num
    }
    
    // Get display label for cluster (handle noise cluster from OPTICS)
    const getClusterLabel = (cluster) => {
      if (!cluster) return 'Unknown'
      if (cluster.id === -1 || cluster.id === '-1') {
        return '🔸 Noise (Outliers)'
      }
      return cluster.interpretation?.label || `Cluster ${cluster.id}`
    }

    // Check if cluster is active (handles type coercion properly)
    const isClusterActive = (clusterId) => {
      const normalizedCluster = normalizeId(clusterId)
      const normalizedSelected = normalizeId(selectedClusterId.value)
      return normalizedCluster === normalizedSelected
    }

    // Select cluster method
    const selectCluster = (clusterId) => {
      selectedClusterId.value = normalizeId(clusterId)
    }

    const activeCluster = computed(() => {
      // Explicitly check for null/undefined, but allow 0
      if (selectedClusterId.value === null || selectedClusterId.value === undefined) {
        return null
      }
      
      if (!props.clusters || props.clusters.length === 0) {
        return null
      }
      
      // Find cluster with normalized comparison
      const normalizedSelected = normalizeId(selectedClusterId.value)
      const found = props.clusters.find(cluster => {
        return normalizeId(cluster.id) === normalizedSelected
      })
      
      return found || null
    })

    // Filtered and sorted members
    const filteredMembers = computed(() => {
      if (!activeCluster.value || !activeCluster.value.members) {
        return []
      }

      let members = [...activeCluster.value.members]

      // Apply search filter
      if (searchQuery.value.trim()) {
        const query = searchQuery.value.toLowerCase().trim()
        members = members.filter(member => {
          const cityName = (member.kabupaten_kota || '').toLowerCase()
          const provinceName = (member.provinsi || '').toLowerCase()
          return cityName.includes(query) || provinceName.includes(query)
        })
      }

      // Apply sorting
      members.sort((a, b) => {
        switch (sortBy.value) {
          case 'name-asc':
            return (a.kabupaten_kota || '').localeCompare(b.kabupaten_kota || '')
          case 'name-desc':
            return (b.kabupaten_kota || '').localeCompare(a.kabupaten_kota || '')
          case 'ipm-asc':
            return (a.ipm || 0) - (b.ipm || 0)
          case 'ipm-desc':
            return (b.ipm || 0) - (a.ipm || 0)
          case 'poverty-asc':
            return (a.garis_kemiskinan || 0) - (b.garis_kemiskinan || 0)
          case 'poverty-desc':
            return (b.garis_kemiskinan || 0) - (a.garis_kemiskinan || 0)
          case 'expenditure-asc':
            return (a.pengeluaran_per_kapita || 0) - (b.pengeluaran_per_kapita || 0)
          case 'expenditure-desc':
            return (b.pengeluaran_per_kapita || 0) - (a.pengeluaran_per_kapita || 0)
          case 'membership-asc':
            return (a.membership || 0) - (b.membership || 0)
          case 'membership-desc':
            return (b.membership || 0) - (a.membership || 0)
          default:
            return 0
        }
      })

      return members
    })

    const formatCurrency = (value) => {
      if (!value) return 'N/A'
      return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
      }).format(value)
    }

    const getInterpretationIcon = (category) => {
      const icons = {
        'poor': '⚠️',
        'prosperous': '✨',
        'vulnerable': '⚡',
        'developing': '📈',
        'middle': '🔄'
      }
      return icons[category] || '📊'
    }

    // Initialize with first cluster - always select first cluster when clusters change
    watch(() => props.clusters, (newClusters) => {
      if (newClusters && newClusters.length > 0) {
        // Always reset to first cluster when data changes
        selectedClusterId.value = normalizeId(newClusters[0].id)
      }
    }, { immediate: true })

    return {
      selectedClusterId,
      activeCluster,
      searchQuery,
      sortBy,
      filteredMembers,
      getClusterColor,
      formatCurrency,
      selectCluster,
      isClusterActive,
      normalizeId,
      getClusterLabel,
      getInterpretationIcon
    }
  }
}
</script>

<style scoped>
.cluster-detail-card {
  margin-bottom: 2rem;
}

.cluster-tabs {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

.cluster-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.cluster-tab:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.cluster-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: #667eea;
}

.tab-color {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid white;
}

.cluster-detail {
  display: grid;
  gap: 2rem;
}

.cluster-info h4 {
  font-size: 1.5rem;
  color: #2d3748;
  margin-bottom: 1.5rem;
}

.cluster-stats {
  background: #f7fafc;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  margin-bottom: 1rem;
}

.stat-label {
  font-weight: 600;
  color: #4a5568;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #667eea;
}

.centroid-info {
  margin-top: 1.5rem;
}

.centroid-info h5 {
  font-size: 1.1rem;
  color: #2d3748;
  margin-bottom: 1rem;
}

.centroid-values {
  display: grid;
  gap: 0.75rem;
}

.centroid-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: white;
  border-radius: 6px;
  border-left: 3px solid #667eea;
}

.centroid-item span:first-child {
  font-weight: 600;
  color: #4a5568;
}

.centroid-item span:last-child {
  font-weight: 700;
  color: #2d3748;
}

.members-header {
  margin-bottom: 1.5rem;
}

.members-header h5 {
  font-size: 1.2rem;
  color: #2d3748;
  margin-bottom: 1rem;
}

.members-controls {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: center;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 250px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1rem;
  color: #718096;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 2.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  background: white;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.search-input::placeholder {
  color: #a0aec0;
}

.clear-search {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: #718096;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s ease;
  line-height: 1;
}

.clear-search:hover {
  background: #f7fafc;
  color: #e53e3e;
}

.sort-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sort-box label {
  font-weight: 600;
  color: #4a5568;
  font-size: 0.95rem;
  white-space: nowrap;
}

.sort-select {
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 200px;
}

.sort-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.sort-select:hover {
  border-color: #cbd5e0;
}

.no-results {
  text-align: center;
  padding: 3rem 1.5rem;
  background: #f7fafc;
  border-radius: 8px;
  border: 2px dashed #cbd5e0;
}

.no-results p {
  color: #718096;
  font-size: 1rem;
  margin: 0;
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.member-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.member-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
  transform: translateY(-2px);
}

.member-card h6 {
  font-size: 1.1rem;
  color: #2d3748;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.member-province {
  font-size: 0.9rem;
  color: #718096;
  margin-bottom: 1rem;
}

.member-stats {
  display: grid;
  gap: 0.75rem;
}

.member-stat {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background: #f7fafc;
  border-radius: 6px;
}

.member-stat span:first-child {
  font-size: 0.9rem;
  color: #4a5568;
  font-weight: 500;
}

.member-stat span:last-child {
  font-weight: 700;
  color: #2d3748;
}

.membership-stat {
  flex-direction: column;
  gap: 0.5rem;
}

.membership-bar-mini {
  position: relative;
  width: 100%;
  height: 24px;
  background: #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
}

.membership-fill-mini {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
}

.membership-text-mini {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  font-size: 0.85rem;
  font-weight: 700;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

@media (max-width: 768px) {
  .members-grid {
    grid-template-columns: 1fr;
  }
  
  .cluster-tabs {
    flex-direction: column;
  }
  
  .cluster-tab {
    width: 100%;
  }

  .members-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    min-width: 100%;
  }

  .sort-box {
    flex-direction: column;
    align-items: stretch;
  }

  .sort-box label {
    font-size: 0.875rem;
  }

  .sort-select {
    width: 100%;
  }
}
</style>
