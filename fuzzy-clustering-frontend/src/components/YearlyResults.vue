<template>
  <div class="yearly-results">
    <div class="results-header">
      <h2>📅 Hasil Clustering Per Tahun</h2>
      <p>Analisis clustering dilakukan secara terpisah untuk setiap tahun</p>
    </div>

    <!-- Overall Summary -->
    <div class="overall-summary card">
      <h3>📊 Ringkasan Keseluruhan</h3>
      <div class="summary-grid">
        <div class="summary-item">
          <div class="summary-icon">🔬</div>
          <div class="summary-content">
            <h4>{{ results.overall_summary.algorithm }}</h4>
            <p>Algoritma yang digunakan</p>
          </div>
        </div>
        <div class="summary-item">
          <div class="summary-icon">📅</div>
          <div class="summary-content">
            <h4>{{ results.overall_summary.total_years }}</h4>
            <p>Total tahun diproses</p>
          </div>
        </div>
        <div class="summary-item">
          <div class="summary-icon">✅</div>
          <div class="summary-content">
            <h4>{{ results.overall_summary.successful_years }}</h4>
            <p>Tahun berhasil</p>
          </div>
        </div>
        <div class="summary-item">
          <div class="summary-icon">📈</div>
          <div class="summary-content">
            <h4>{{ (results.overall_summary.success_rate * 100).toFixed(1) }}%</h4>
            <p>Tingkat keberhasilan</p>
          </div>
        </div>
      </div>

      <!-- Average Evaluation Metrics -->
      <div v-if="results.overall_summary.average_evaluation" class="average-metrics">
        <h4>📊 Rata-rata Metrik Evaluasi</h4>
        <div class="metrics-grid">
          <div class="metric-card">
            <h5>Davies-Bouldin Index</h5>
            <div class="metric-value">
              {{ results.overall_summary.average_evaluation.davies_bouldin?.toFixed(4) || 'N/A' }}
            </div>
            <div class="metric-quality">
              <span :class="getDBIQuality(results.overall_summary.average_evaluation.davies_bouldin)">
                {{ getDBIQualityText(results.overall_summary.average_evaluation.davies_bouldin) }}
              </span>
            </div>
          </div>
          <div class="metric-card">
            <h5>Silhouette Score</h5>
            <div class="metric-value">
              {{ results.overall_summary.average_evaluation.silhouette_score?.toFixed(4) || 'N/A' }}
            </div>
            <div class="metric-quality">
              <span :class="getSilhouetteQuality(results.overall_summary.average_evaluation.silhouette_score)">
                {{ getSilhouetteQualityText(results.overall_summary.average_evaluation.silhouette_score) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Year Selection -->
    <div class="year-selection card">
      <h3>🎯 Pilih Tahun untuk Analisis Detail</h3>
      <div class="year-tabs">
        <button 
          v-for="year in availableYears" 
          :key="year"
          @click="selectedYear = year"
          :class="['year-tab', { active: selectedYear === year, error: hasError(year) }]"
        >
          {{ year }}
          <span v-if="hasError(year)" class="error-indicator">❌</span>
          <span v-else class="success-indicator">✅</span>
        </button>
      </div>
      <p class="year-info">
        {{ selectedYear ? `Menampilkan hasil clustering untuk tahun ${selectedYear}` : 'Pilih tahun untuk melihat detail' }}
      </p>
    </div>

    <!-- Error State for Selected Year -->
    <div v-if="selectedYear && selectedYearResults && selectedYearResults.error" class="error-card card">
      <h3>❌ Error untuk Tahun {{ selectedYear }}</h3>
      <p>{{ selectedYearResults.error }}</p>
    </div>

    <!-- Selected Year Results -->
    <div v-if="selectedYear && selectedYearResults && !selectedYearResults.error" class="selected-year-results">
        <!-- Year Summary -->
        <div class="year-summary card">
          <h3>📊 Ringkasan Tahun {{ selectedYear }}</h3>
          <div class="year-stats">
            <div class="stat-item">
              <span class="stat-label">Total Daerah:</span>
              <span class="stat-value">{{ selectedYearResults.summary.total_regions }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Jumlah Cluster:</span>
              <span class="stat-value">{{ selectedYearResults.summary.num_clusters }}</span>
            </div>
            <div v-if="selectedYearResults.summary.noise_points !== undefined" class="stat-item">
              <span class="stat-label">Noise Points:</span>
              <span class="stat-value">{{ selectedYearResults.summary.noise_points }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Waktu Eksekusi:</span>
              <span class="stat-value">{{ selectedYearResults.summary.execution_time?.toFixed(2) }}s</span>
            </div>
          </div>

          <!-- Year Evaluation Metrics -->
          <div class="year-evaluation">
            <h4>📈 Metrik Evaluasi</h4>
            <div class="metrics-grid">
              <div class="metric-card">
                <h5>Davies-Bouldin Index</h5>
                <div class="metric-value">
                  {{ selectedYearResults.evaluation.davies_bouldin?.toFixed(4) || 'N/A' }}
                </div>
                <div class="metric-quality">
                  <span :class="getDBIQuality(selectedYearResults.evaluation.davies_bouldin)">
                    {{ getDBIQualityText(selectedYearResults.evaluation.davies_bouldin) }}
                  </span>
                </div>
              </div>
              <div class="metric-card">
                <h5>Silhouette Score</h5>
                <div class="metric-value">
                  {{ selectedYearResults.evaluation.silhouette_score?.toFixed(4) || 'N/A' }}
                </div>
                <div class="metric-quality">
                  <span :class="getSilhouetteQuality(selectedYearResults.evaluation.silhouette_score)">
                    {{ getSilhouetteQualityText(selectedYearResults.evaluation.silhouette_score) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Visualizations for Selected Year -->
        <div v-if="selectedYearResults.clusters && selectedYearResults.clusters.length > 0" class="year-visualizations">
          <CorrelationMatrix 
            :clusters="selectedYearResults.clusters" 
            :title="`Analisis Korelasi Variabel - ${selectedYearResults.algorithm} (${selectedYear})`"
          />
          
          <ScatterPlot 
            :clusters="selectedYearResults.clusters" 
            :title="`Scatter Plot - ${selectedYearResults.algorithm} Clustering (${selectedYear})`"
          />
          
          <BoxPlot 
            :clusters="selectedYearResults.clusters" 
            :title="`Analisis Distribusi - ${selectedYearResults.algorithm} (${selectedYear})`"
          />
          
          <InteractiveMap 
            :clusters="selectedYearResults.clusters" 
            :title="`Peta Sebaran Cluster - ${selectedYearResults.algorithm} (${selectedYear})`"
          />
        </div>

        <!-- Cluster Details for Selected Year -->
        <div v-if="selectedYearResults.clusters && selectedYearResults.clusters.length > 0" class="year-cluster-details card">
          <h3>🔍 Detail Cluster Tahun {{ selectedYear }}</h3>
          <div class="cluster-tabs">
            <button 
              v-for="(cluster, index) in selectedYearResults.clusters" 
              :key="cluster.id"
              @click="selectedCluster = cluster.id"
              :class="['cluster-tab', { active: selectedCluster === cluster.id }]"
              :style="{ borderColor: getClusterColor(index) }"
            >
              <div class="tab-color" :style="{ backgroundColor: getClusterColor(index) }"></div>
              Cluster {{ cluster.id }} ({{ cluster.size }})
            </button>
          </div>
          
          <div v-if="activeCluster" class="cluster-detail">
            <div class="cluster-info">
              <h4>Cluster {{ activeCluster.id }} - Tahun {{ selectedYear }}</h4>
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
                      <span>{{ activeCluster.centroid.ipm?.toFixed(2) }}</span>
                    </div>
                    <div class="centroid-item">
                      <span>Garis Kemiskinan:</span>
                      <span>{{ formatCurrency(activeCluster.centroid.garis_kemiskinan) }}</span>
                    </div>
                    <div class="centroid-item">
                      <span>Pengeluaran Per Kapita:</span>
                      <span>{{ formatCurrency(activeCluster.centroid.pengeluaran_per_kapita) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="cluster-members">
              <div class="members-header">
                <h5>Daftar Daerah:</h5>
                <div class="sort-controls">
                  <label for="yearly-sort-field">Urutkan:</label>
                  <select id="yearly-sort-field" v-model="sortField" class="sort-select">
                    <option value="kabupaten_kota">Nama Daerah</option>
                    <option value="ipm">IPM</option>
                    <option value="garis_kemiskinan">Garis Kemiskinan</option>
                    <option value="pengeluaran_per_kapita">Pengeluaran Per Kapita</option>
                    <option v-if="selectedYearResults?.algorithm === 'Fuzzy C-Means'" value="membership">Membership</option>
                  </select>
                  <button @click="toggleSortOrder" class="sort-order-btn" :title="sortOrder === 'asc' ? 'Urutkan Menurun' : 'Urutkan Menaik'">
                    <span v-if="sortOrder === 'asc'">↑</span>
                    <span v-else>↓</span>
                  </button>
                </div>
              </div>
              <div class="members-grid">
                <div 
                  v-for="member in sortedClusterMembers" 
                  :key="member.kabupaten_kota"
                  class="member-card"
                >
                  <h6>{{ member.kabupaten_kota }}</h6>
                  <div class="member-stats">
                    <div class="member-stat">
                      <span>IPM:</span>
                      <span>{{ member.ipm?.toFixed(2) }}</span>
                    </div>
                    <div class="member-stat">
                      <span>Garis Kemiskinan:</span>
                      <span>{{ formatCurrency(member.garis_kemiskinan) }}</span>
                    </div>
                    <div class="member-stat">
                      <span>Pengeluaran:</span>
                      <span>{{ formatCurrency(member.pengeluaran_per_kapita) }}</span>
                    </div>
                    <div v-if="member.membership && member.membership < 1.0" class="member-stat">
                      <span>Membership:</span>
                      <span>{{ (member.membership * 100).toFixed(1) }}%</span>
                    </div>
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
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import ScatterPlot from './ScatterPlot.vue'
import BoxPlot from './BoxPlot.vue'
import InteractiveMap from './InteractiveMap.vue'
import CorrelationMatrix from './CorrelationMatrix.vue'

export default {
  name: 'YearlyResults',
  components: {
    ScatterPlot,
    BoxPlot,
    InteractiveMap,
    CorrelationMatrix
  },
  props: {
    results: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const selectedYear = ref(null)
    const selectedCluster = ref(null)
    const sortField = ref('kabupaten_kota')
    const sortOrder = ref('asc')

    const colors = [
      '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
      '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
    ]

    const availableYears = computed(() => {
      if (!props.results?.results_per_year) return []
      return Object.keys(props.results.results_per_year).sort()
    })

    const selectedYearResults = computed(() => {
      if (!selectedYear.value || !props.results?.results_per_year) return null
      const yearResults = props.results.results_per_year[selectedYear.value]
      
      // Debug logging
      console.log(`🔍 YearlyResults Debug for year ${selectedYear.value}:`)
      console.log('Year results:', yearResults)
      if (yearResults?.clusters) {
        console.log(`Found ${yearResults.clusters.length} clusters:`)
        yearResults.clusters.forEach((cluster, index) => {
          console.log(`  Cluster ${cluster.id}: ${cluster.size} members`)
        })
      } else {
        console.log('No clusters found in year results')
      }
      
      return yearResults
    })

    const activeCluster = computed(() => {
      if (selectedCluster.value === null || selectedCluster.value === undefined || !selectedYearResults.value?.clusters) return null
      
      // Handle both string and number cluster IDs
      const clusterId = selectedCluster.value
      const found = selectedYearResults.value.clusters.find(cluster => 
        cluster.id === clusterId || 
        cluster.id === String(clusterId) || 
        cluster.id === Number(clusterId)
      )
      
      console.log('🔍 YearlyResults ActiveCluster Debug:', {
        selectedClusterId: selectedCluster.value,
        availableClusters: selectedYearResults.value?.clusters?.map(c => ({ id: c.id, size: c.size })) || [],
        foundCluster: found ? { id: found.id, size: found.size } : null
      })
      
      return found
    })

    const sortedClusterMembers = computed(() => {
      if (!activeCluster.value || !activeCluster.value.members) return []
      
      const members = [...activeCluster.value.members]
      
      return members.sort((a, b) => {
        let aValue = a[sortField.value]
        let bValue = b[sortField.value]
        
        // Handle null/undefined values
        if (aValue == null) aValue = ''
        if (bValue == null) bValue = ''
        
        // Convert to appropriate type for comparison
        if (typeof aValue === 'string' && typeof bValue === 'string') {
          aValue = aValue.toLowerCase()
          bValue = bValue.toLowerCase()
        }
        
        let comparison = 0
        if (aValue < bValue) {
          comparison = -1
        } else if (aValue > bValue) {
          comparison = 1
        }
        
        return sortOrder.value === 'asc' ? comparison : -comparison
      })
    })

    const hasError = (year) => {
      return props.results?.results_per_year?.[year]?.error !== undefined
    }

    const getClusterColor = (index) => {
      return colors[index % colors.length]
    }

    const formatCurrency = (value) => {
      if (!value) return 'N/A'
      return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
      }).format(value)
    }

    const getDBIQuality = (score) => {
      if (!score || score === null) return 'quality-unknown'
      if (score < 1) return 'quality-excellent'
      if (score < 1.5) return 'quality-good'
      if (score < 2) return 'quality-fair'
      return 'quality-poor'
    }

    const getDBIQualityText = (score) => {
      if (!score || score === null) return 'Tidak tersedia'
      if (score < 1) return 'Sangat Baik'
      if (score < 1.5) return 'Baik'
      if (score < 2) return 'Cukup'
      return 'Perlu Perbaikan'
    }

    const getSilhouetteQuality = (score) => {
      if (!score || score === null) return 'quality-unknown'
      if (score > 0.7) return 'quality-excellent'
      if (score > 0.5) return 'quality-good'
      if (score > 0.25) return 'quality-fair'
      return 'quality-poor'
    }

    const getSilhouetteQualityText = (score) => {
      if (!score || score === null) return 'Tidak tersedia'
      if (score > 0.7) return 'Sangat Baik'
      if (score > 0.5) return 'Baik'
      if (score > 0.25) return 'Cukup'
      return 'Perlu Perbaikan'
    }

    const toggleSortOrder = () => {
      sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
    }

    // Set default selected year when component mounts or data changes
    const setDefaultYear = async () => {
      await nextTick()
      try {
        if (availableYears.value && availableYears.value.length > 0 && !selectedYear.value) {
          selectedYear.value = availableYears.value[availableYears.value.length - 1] // Latest year
        }
      } catch (error) {
        console.warn('Error setting default year in YearlyResults:', error)
      }
    }

    onMounted(() => {
      setDefaultYear()
    })

    // Watch for data changes and reset selected year if needed
    watch(() => props.results, () => {
      setDefaultYear()
    }, { deep: true })

    // Watch for year changes and set default cluster
    watch(() => selectedYearResults.value, (newYearResults) => {
      if (newYearResults?.clusters && newYearResults.clusters.length > 0) {
        // Auto-select first cluster if none is selected or current selection is invalid
        const currentClusterExists = newYearResults.clusters.some(cluster => 
          cluster.id === selectedCluster.value || 
          cluster.id === String(selectedCluster.value) || 
          cluster.id === Number(selectedCluster.value)
        )
        
        if (!currentClusterExists) {
          selectedCluster.value = newYearResults.clusters[0].id
          console.log('🎯 YearlyResults: Auto-selected first cluster:', selectedCluster.value)
        }
      } else {
        selectedCluster.value = null
        console.log('❌ YearlyResults: No clusters available, clearing selection')
      }
    }, { deep: true })

    return {
      selectedYear,
      selectedCluster,
      sortField,
      sortOrder,
      availableYears,
      selectedYearResults,
      activeCluster,
      sortedClusterMembers,
      hasError,
      getClusterColor,
      formatCurrency,
      getDBIQuality,
      getDBIQualityText,
      getSilhouetteQuality,
      getSilhouetteQualityText,
      toggleSortOrder
    }
  }
}
</script>

<style scoped>
.yearly-results {
  padding: 2rem 0;
}

.results-header {
  text-align: center;
  margin-bottom: 2rem;
}

.results-header h2 {
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.results-header p {
  color: #718096;
}

.overall-summary {
  margin-bottom: 2rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f7fafc;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.summary-icon {
  font-size: 2rem;
}

.summary-content h4 {
  color: #2d3748;
  margin: 0;
  font-size: 1.5rem;
}

.summary-content p {
  color: #718096;
  margin: 0.25rem 0 0 0;
  font-size: 0.875rem;
}

.average-metrics {
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.average-metrics h4 {
  color: #4a5568;
  margin-bottom: 1rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.metric-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  text-align: center;
}

.metric-card h5 {
  color: #4a5568;
  margin-bottom: 1rem;
}

.metric-value {
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.metric-quality {
  font-size: 0.875rem;
}

.quality-excellent { color: #38a169; font-weight: 600; }
.quality-good { color: #3182ce; font-weight: 600; }
.quality-fair { color: #d69e2e; font-weight: 600; }
.quality-poor { color: #e53e3e; font-weight: 600; }
.quality-unknown { color: #718096; font-weight: 600; }

.year-selection {
  margin-bottom: 2rem;
}

.year-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.year-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  background: white;
  color: #4a5568;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.year-tab:hover {
  border-color: #667eea;
  color: #667eea;
}

.year-tab.active {
  background: #667eea;
  border-color: #667eea;
  color: white;
}

.year-tab.error {
  border-color: #e53e3e;
  color: #e53e3e;
}

.year-tab.error.active {
  background: #e53e3e;
  color: white;
}

.success-indicator, .error-indicator {
  font-size: 0.75rem;
}

.year-info {
  color: #718096;
  font-size: 0.875rem;
  margin: 0;
}

.error-card {
  background: #fed7d7;
  border: 1px solid #fc8181;
  color: #742a2a;
}

.year-summary {
  margin-bottom: 2rem;
}

.year-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f7fafc;
  border-radius: 6px;
}

.stat-label {
  font-weight: 600;
  color: #4a5568;
}

.stat-value {
  color: #2d3748;
  font-weight: 600;
}

.year-evaluation {
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.year-evaluation h4 {
  color: #4a5568;
  margin-bottom: 1rem;
}

.year-visualizations {
  margin: 2rem 0;
}

.cluster-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 1rem;
}

.cluster-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  background: white;
  color: #4a5568;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.cluster-tab:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.cluster-tab.active {
  background: #f7fafc;
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tab-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.cluster-detail {
  display: grid;
  gap: 2rem;
}

.cluster-info {
  background: #f7fafc;
  padding: 2rem;
  border-radius: 8px;
}

.cluster-info h4 {
  color: #2d3748;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.cluster-stats {
  display: grid;
  gap: 1rem;
}

.centroid-info h5 {
  color: #4a5568;
  margin-bottom: 0.5rem;
}

.centroid-values {
  display: grid;
  gap: 0.5rem;
  padding-left: 1rem;
}

.centroid-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.25rem 0;
  font-size: 0.875rem;
}

.members-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.members-header h5 {
  color: #2d3748;
  margin: 0;
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.sort-controls label {
  color: #4a5568;
  font-weight: 500;
}

.sort-select {
  padding: 0.25rem 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  background: white;
  color: #4a5568;
  font-size: 0.875rem;
}

.sort-order-btn {
  padding: 0.25rem 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  background: white;
  color: #4a5568;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: all 0.2s ease;
}

.sort-order-btn:hover {
  background: #f7fafc;
  border-color: #667eea;
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

.member-card {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.member-card h6 {
  color: #2d3748;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.member-stats {
  display: grid;
  gap: 0.5rem;
}

.member-stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
}

.member-stat span:first-child {
  color: #718096;
  font-weight: 500;
}

.member-stat span:last-child {
  color: #2d3748;
  font-weight: 600;
}

@media (max-width: 768px) {
  .yearly-results {
    padding: 1rem 0;
  }
  
  .summary-grid {
    grid-template-columns: 1fr;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .year-tabs {
    flex-direction: column;
  }
  
  .year-stats {
    grid-template-columns: 1fr;
  }
  
  .cluster-tabs {
    flex-direction: column;
  }
  
  .members-grid {
    grid-template-columns: 1fr;
  }
}
</style>