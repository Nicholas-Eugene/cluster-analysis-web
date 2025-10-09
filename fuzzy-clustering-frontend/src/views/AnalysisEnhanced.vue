<template>
  <div class="analysis-page">
    <div class="container">
      <!-- Header Section -->
      <div class="page-header">
        <h1>Hasil Analisis Clustering</h1>
        <p v-if="results">
          Analisis menggunakan algoritma <strong>{{ results.algorithm }}</strong>
          {{ results.summary.selectedYear ? `untuk tahun ${results.summary.selectedYear}` : 'untuk semua tahun (2015-2024)' }}
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>Memuat hasil analisis...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="error-container">
        <div class="alert alert-error">
          <h3>❌ Terjadi Kesalahan</h3>
          <p>{{ error }}</p>
          <button @click="$router.push('/upload')" class="btn btn-primary">
            🔄 Kembali ke Upload
          </button>
        </div>
      </div>

      <!-- Results Section -->
      <div v-if="results && !isLoading" class="results-section">
        
        <!-- Per Year Results -->
        <div v-if="results.clustering_type === 'per_year'">
          <YearlyResults :results="results" />
        </div>
        
        <!-- Single Year Results (Legacy) -->
        <div v-else class="single-year-results">
          <!-- Summary Cards -->
          <div class="summary-cards">
            <div class="summary-card">
              <div class="card-icon">📊</div>
              <div class="card-content">
                <h3>{{ results.summary.total_regions }}</h3>
                <p>Total Daerah</p>
              </div>
            </div>
            
            <div class="summary-card">
              <div class="card-icon">🎯</div>
              <div class="card-content">
                <h3>{{ results.summary.num_clusters }}</h3>
                <p>Jumlah Cluster</p>
              </div>
            </div>
            
            <div class="summary-card">
              <div class="card-icon">⏱️</div>
              <div class="card-content">
                <h3>{{ results.summary.execution_time?.toFixed(2) }}s</h3>
                <p>Waktu Eksekusi</p>
              </div>
            </div>
            
            <div v-if="results.summary.iterations" class="summary-card">
              <div class="card-icon">🔄</div>
              <div class="card-content">
                <h3>{{ results.summary.iterations }}</h3>
                <p>Iterasi</p>
              </div>
            </div>
          </div>

        <!-- Evaluation Metrics -->
        <div class="card">
          <h2>📈 Metrik Evaluasi</h2>
          <div class="evaluation-metrics">
            <div class="metric-card">
              <h3>Davies-Bouldin Index</h3>
              <div class="metric-value">
                {{ results.evaluation.davies_bouldin?.toFixed(4) || 'N/A' }}
              </div>
              <p class="metric-description">
                Semakin rendah semakin baik. Mengukur rasio antara jarak dalam cluster dan antar cluster.
              </p>
              <div class="metric-quality">
                <span class="quality-label">Kualitas:</span>
                <span :class="getDBIQuality(results.evaluation.davies_bouldin)">
                  {{ getDBIQualityText(results.evaluation.davies_bouldin) }}
                </span>
              </div>
            </div>
            
            <div class="metric-card">
              <h3>Silhouette Score</h3>
              <div class="metric-value">
                {{ results.evaluation.silhouette_score?.toFixed(4) || 'N/A' }}
              </div>
              <p class="metric-description">
                Rentang -1 hingga 1. Semakin tinggi semakin baik. Mengukur seberapa mirip objek dengan clusternya.
              </p>
              <div class="metric-quality">
                <span class="quality-label">Kualitas:</span>
                <span :class="getSilhouetteQuality(results.evaluation.silhouette_score)">
                  {{ getSilhouetteQualityText(results.evaluation.silhouette_score) }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Year Selector for Multi-Year Analysis -->
        <div v-if="!results.summary.selectedYear && availableYears.length > 1" class="card">
          <h2>📅 Filter Tahun</h2>
          <div class="year-selector">
            <div class="year-controls">
              <button 
                v-for="year in availableYears" 
                :key="year"
                @click="selectedYear = year"
                :class="['year-btn', { active: selectedYear === year }]"
              >
                {{ year }}
              </button>
              <button 
                @click="selectedYear = null"
                :class="['year-btn', { active: selectedYear === null }]"
              >
                Semua Tahun
              </button>
            </div>
            <p class="year-info">
              {{ selectedYear ? `Menampilkan data untuk tahun ${selectedYear}` : 'Menampilkan data untuk semua tahun' }}
            </p>
          </div>
        </div>

        <!-- Visualizations -->
        <div class="visualizations">
          
          <!-- Scatter Plot -->
          <ScatterPlot 
            :clusters="filteredClusters" 
            :title="`Scatter Plot - ${results.algorithm} Clustering`"
          />
          
          <!-- Box Plot -->
          <BoxPlot 
            :clusters="filteredClusters" 
            :title="`Analisis Distribusi per Cluster - ${results.algorithm}`"
          />
          
          <!-- Interactive Map -->
          <InteractiveMap 
            :clusters="filteredClusters" 
            :title="`Peta Sebaran Cluster - ${results.algorithm}`"
          />
          
        </div>

        <!-- Cluster Details -->
        <div class="card">
          <h2>🔍 Detail Cluster</h2>
          <div class="cluster-tabs">
            <button 
              v-for="(cluster, index) in filteredClusters" 
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
              <h3>Cluster {{ activeCluster.id }}</h3>
              <div class="cluster-stats">
                <div class="stat-item">
                  <span class="stat-label">Jumlah Daerah:</span>
                  <span class="stat-value">{{ activeCluster.size }}</span>
                </div>
                <div v-if="activeCluster.centroid" class="centroid-info">
                  <h4>Centroid (Rata-rata):</h4>
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
              <h4>Daftar Daerah:</h4>
              <div class="members-table-container">
                <table class="members-table">
                  <thead>
                    <tr>
                      <th>Kabupaten/Kota</th>
                      <th>Provinsi</th>
                      <th>Tahun</th>
                      <th>IPM</th>
                      <th>Garis Kemiskinan</th>
                      <th>Pengeluaran Per Kapita</th>
                      <th v-if="results.algorithm === 'Fuzzy C-Means'">Membership</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="member in activeCluster.members" :key="`${member.kabupaten_kota}-${member.tahun}`">
                      <td>{{ member.kabupaten_kota }}</td>
                      <td>{{ member.provinsi || 'N/A' }}</td>
                      <td>{{ member.tahun }}</td>
                      <td>{{ member.ipm?.toFixed(2) }}</td>
                      <td>{{ formatCurrency(member.garis_kemiskinan) }}</td>
                      <td>{{ formatCurrency(member.pengeluaran_per_kapita) }}</td>
                      <td v-if="results.algorithm === 'Fuzzy C-Means'">
                        <div class="membership-bar">
                          <div 
                            class="membership-fill" 
                            :style="{ 
                              width: `${(member.membership * 100)}%`,
                              backgroundColor: getClusterColor(filteredClusters.findIndex(c => c.id === activeCluster.id))
                            }"
                          ></div>
                          <span class="membership-text">{{ (member.membership * 100).toFixed(1) }}%</span>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

          <!-- Export Options -->
          <div class="card">
            <h2>📥 Export Hasil</h2>
            <div class="export-options">
              <button @click="exportToCSV" class="btn btn-secondary">
                📊 Export ke CSV
              </button>
              <button @click="exportToJSON" class="btn btn-secondary">
                📄 Export ke JSON
              </button>
              <button @click="generateReport" class="btn btn-primary">
                📋 Generate Report
              </button>
            </div>
          </div>
        </div>
        <!-- End Single Year Results -->

      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ScatterPlot from '../components/ScatterPlot.vue'
import BoxPlot from '../components/BoxPlot.vue'
import InteractiveMap from '../components/InteractiveMap.vue'
import YearlyResults from '../components/YearlyResults.vue'
import apiService from '../services/apiService.js'

export default {
  name: 'AnalysisEnhanced',
  components: {
    ScatterPlot,
    BoxPlot,
    InteractiveMap,
    YearlyResults
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const isLoading = ref(true)
    const error = ref('')
    const results = ref(null)
    const selectedYear = ref(null)
    const selectedCluster = ref(null)

    const colors = [
      '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
      '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
    ]

    const getClusterColor = (index) => {
      return colors[index % colors.length]
    }

    const availableYears = computed(() => {
      if (!results.value || !results.value.clusters) return []
      
      const years = new Set()
      results.value.clusters.forEach(cluster => {
        cluster.members.forEach(member => {
          if (member.tahun) years.add(member.tahun)
        })
      })
      
      return Array.from(years).sort()
    })

    const filteredClusters = computed(() => {
      if (!results.value || !results.value.clusters) return []
      
      if (!selectedYear.value) return results.value.clusters
      
      return results.value.clusters.map(cluster => ({
        ...cluster,
        members: cluster.members.filter(member => member.tahun === selectedYear.value),
        size: cluster.members.filter(member => member.tahun === selectedYear.value).length
      })).filter(cluster => cluster.size > 0)
    })

    const activeCluster = computed(() => {
      if (!selectedCluster.value || !filteredClusters.value) return null
      return filteredClusters.value.find(cluster => cluster.id === selectedCluster.value)
    })

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

    const loadResults = async () => {
      try {
        isLoading.value = true
        error.value = ''
        
        const sessionId = route.query.sessionId
        if (!sessionId) {
          throw new Error('Session ID tidak ditemukan')
        }

        const data = await apiService.getResults(sessionId)
        results.value = data
        
        // Set default selected cluster
        if (data.clusters && data.clusters.length > 0) {
          selectedCluster.value = data.clusters[0].id
        }
        
      } catch (err) {
        error.value = err.message || 'Gagal memuat hasil analisis'
      } finally {
        isLoading.value = false
      }
    }

    const exportToCSV = () => {
      if (!results.value) return
      
      const csvData = []
      const headers = [
        'Cluster', 'Kabupaten/Kota', 'Provinsi', 'Tahun', 
        'IPM', 'Garis Kemiskinan', 'Pengeluaran Per Kapita'
      ]
      
      if (results.value.algorithm === 'Fuzzy C-Means') {
        headers.push('Membership')
      }
      
      csvData.push(headers.join(','))
      
      filteredClusters.value.forEach(cluster => {
        cluster.members.forEach(member => {
          const row = [
            cluster.id,
            `"${member.kabupaten_kota}"`,
            `"${member.provinsi || 'N/A'}"`,
            member.tahun,
            member.ipm?.toFixed(2) || 'N/A',
            member.garis_kemiskinan || 'N/A',
            member.pengeluaran_per_kapita || 'N/A'
          ]
          
          if (results.value.algorithm === 'Fuzzy C-Means') {
            row.push((member.membership * 100).toFixed(2))
          }
          
          csvData.push(row.join(','))
        })
      })
      
      const blob = new Blob([csvData.join('\n')], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `clustering_results_${results.value.algorithm.toLowerCase()}_${Date.now()}.csv`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    }

    const exportToJSON = () => {
      if (!results.value) return
      
      const exportData = {
        ...results.value,
        clusters: filteredClusters.value,
        export_timestamp: new Date().toISOString()
      }
      
      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `clustering_results_${results.value.algorithm.toLowerCase()}_${Date.now()}.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    }

    const generateReport = () => {
      // This would typically generate a PDF report
      // For now, we'll create a detailed text report
      if (!results.value) return
      
      const reportLines = [
        `LAPORAN ANALISIS CLUSTERING`,
        `Algoritma: ${results.value.algorithm}`,
        `Tanggal: ${new Date().toLocaleDateString('id-ID')}`,
        ``,
        `RINGKASAN:`,
        `- Total Daerah: ${results.value.summary.total_regions}`,
        `- Jumlah Cluster: ${results.value.summary.num_clusters}`,
        `- Waktu Eksekusi: ${results.value.summary.execution_time?.toFixed(2)}s`,
        ``,
        `EVALUASI:`,
        `- Davies-Bouldin Index: ${results.value.evaluation.davies_bouldin?.toFixed(4) || 'N/A'}`,
        `- Silhouette Score: ${results.value.evaluation.silhouette_score?.toFixed(4) || 'N/A'}`,
        ``,
        `DETAIL CLUSTER:`
      ]
      
      filteredClusters.value.forEach(cluster => {
        reportLines.push(``)
        reportLines.push(`Cluster ${cluster.id} (${cluster.size} daerah):`)
        if (cluster.centroid) {
          reportLines.push(`  Centroid:`)
          reportLines.push(`    IPM: ${cluster.centroid.ipm?.toFixed(2)}`)
          reportLines.push(`    Garis Kemiskinan: ${formatCurrency(cluster.centroid.garis_kemiskinan)}`)
          reportLines.push(`    Pengeluaran Per Kapita: ${formatCurrency(cluster.centroid.pengeluaran_per_kapita)}`)
        }
        reportLines.push(`  Anggota:`)
        cluster.members.forEach(member => {
          reportLines.push(`    - ${member.kabupaten_kota} (${member.tahun})`)
        })
      })
      
      const blob = new Blob([reportLines.join('\n')], { type: 'text/plain' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `clustering_report_${results.value.algorithm.toLowerCase()}_${Date.now()}.txt`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    }

    onMounted(() => {
      loadResults()
    })

    watch(() => filteredClusters.value, (newClusters) => {
      if (newClusters.length > 0 && !activeCluster.value) {
        selectedCluster.value = newClusters[0].id
      }
    })

    return {
      isLoading,
      error,
      results,
      selectedYear,
      selectedCluster,
      availableYears,
      filteredClusters,
      activeCluster,
      getClusterColor,
      formatCurrency,
      getDBIQuality,
      getDBIQualityText,
      getSilhouetteQuality,
      getSilhouetteQualityText,
      exportToCSV,
      exportToJSON,
      generateReport
    }
  }
}
</script>

<style scoped>
.analysis-page {
  padding: 2rem 0;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-header h1 {
  font-size: 2.5rem;
  color: #2d3748;
  margin-bottom: 1rem;
}

.page-header p {
  font-size: 1.2rem;
  color: #718096;
}

.loading-container {
  text-align: center;
  padding: 4rem 2rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-left: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  text-align: center;
  padding: 2rem;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.summary-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-icon {
  font-size: 2rem;
  opacity: 0.9;
}

.card-content h3 {
  font-size: 2rem;
  margin: 0;
  font-weight: 700;
}

.card-content p {
  margin: 0.25rem 0 0 0;
  opacity: 0.9;
  font-size: 0.875rem;
}

.evaluation-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 1.5rem;
}

.metric-card {
  background: #f7fafc;
  padding: 2rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  text-align: center;
}

.metric-card h3 {
  color: #2d3748;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 1rem;
}

.metric-description {
  color: #718096;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.metric-quality {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

.quality-label {
  font-weight: 600;
  color: #4a5568;
}

.quality-excellent { color: #38a169; font-weight: 600; }
.quality-good { color: #3182ce; font-weight: 600; }
.quality-fair { color: #d69e2e; font-weight: 600; }
.quality-poor { color: #e53e3e; font-weight: 600; }
.quality-unknown { color: #718096; font-weight: 600; }

.year-selector {
  margin-top: 1.5rem;
}

.year-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.year-btn {
  padding: 0.5rem 1rem;
  border: 2px solid #e2e8f0;
  background: white;
  color: #4a5568;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.year-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.year-btn.active {
  background: #667eea;
  border-color: #667eea;
  color: white;
}

.year-info {
  color: #718096;
  font-size: 0.875rem;
  margin: 0;
}

.visualizations {
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

.cluster-info h3 {
  color: #2d3748;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.cluster-stats {
  display: grid;
  gap: 1rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.stat-label {
  font-weight: 600;
  color: #4a5568;
}

.stat-value {
  color: #2d3748;
  font-weight: 600;
}

.centroid-info h4 {
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

.cluster-members h4 {
  color: #2d3748;
  margin-bottom: 1rem;
}

.members-table-container {
  overflow-x: auto;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.members-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.members-table th,
.members-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
  white-space: nowrap;
}

.members-table th {
  background: #f7fafc;
  font-weight: 600;
  color: #4a5568;
  position: sticky;
  top: 0;
}

.members-table td {
  color: #718096;
}

.membership-bar {
  position: relative;
  background: #e2e8f0;
  border-radius: 4px;
  height: 20px;
  min-width: 80px;
  overflow: hidden;
}

.membership-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.membership-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 0.75rem;
  font-weight: 600;
  color: #2d3748;
}

.export-options {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1.5rem;
}

@media (max-width: 768px) {
  .analysis-page {
    padding: 1rem 0;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .summary-cards {
    grid-template-columns: 1fr;
  }
  
  .evaluation-metrics {
    grid-template-columns: 1fr;
  }
  
  .cluster-tabs {
    flex-direction: column;
  }
  
  .export-options {
    flex-direction: column;
  }
  
  .export-options button {
    width: 100%;
  }
}
</style>