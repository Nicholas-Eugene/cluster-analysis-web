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
        <h4>Cluster {{ activeCluster.id }}</h4>
        <div class="cluster-stats">
          <div class="stat-item">
            <span class="stat-label">Jumlah Daerah:</span>
            <span class="stat-value">{{ activeCluster.size }}</span>
          </div>
          <div v-if="activeCluster.centroid" class="centroid-info">
            <h5>Centroid (Rata-rata):</h5>
            <div class="centroid-values">
              <div class="centroid-item">
                <span>IPM:</span>
                <span>{{ activeCluster.centroid.ipm?.toFixed(2) || 'N/A' }}</span>
              </div>
              <div class="centroid-item">
                <span>Garis Kemiskinan:</span>
                <span>{{ formatCurrency(activeCluster.centroid.garis_kemiskinan) }}</span>
              </div>
              <div class="centroid-item">
                <span>Pengeluaran Per Kapita:</span>
                <span>{{ formatCurrency(activeCluster.centroid.pengeluaran_per_kapita) }} ribu/tahun</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="cluster-members">
        <h5>Daftar Daerah ({{ activeCluster.members.length }}):</h5>
        <div class="members-grid">
          <div 
            v-for="member in activeCluster.members" 
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
                <span>{{ formatCurrency(member.garis_kemiskinan) }} Rp/kapita/bulan</span>
              </div>
              <div class="member-stat">
                <span>Pengeluaran:</span>
                <span>{{ formatCurrency(member.pengeluaran_per_kapita) }}</span>
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

    // Helper to normalize cluster ID (convert to number if possible, handle 0 properly)
    const normalizeId = (id) => {
      // Explicitly handle null/undefined
      if (id === null || id === undefined) return null
      
      // Try to convert to number
      const num = Number(id)
      
      // Return number if it's valid (including 0!), otherwise return original
      return isNaN(num) ? id : num
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
      getClusterColor,
      formatCurrency,
      selectCluster,
      isClusterActive,
      normalizeId,
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

.cluster-members h5 {
  font-size: 1.2rem;
  color: #2d3748;
  margin-bottom: 1.5rem;
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
}
</style>
tyle>
