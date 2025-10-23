<template>
  <div class="analysis-page">
    <div class="container">
      <div class="page-header">
        <div class="header-content">
          <div>
            <h1>Hasil Analisis Clustering</h1>
            <p v-if="results">
              <span v-if="results.clustering_type === 'per_year'">
                Analisis menggunakan algoritma <strong>{{ results.overall_summary.algorithm }}</strong>
                untuk semua tahun ({{ results.overall_summary.years_processed.join(', ') }}) - Mode Per Tahun
              </span>
              <span v-else-if="results.clustering_type === 'all_years_wide'">
                Analisis menggunakan algoritma <strong>{{ results.overall_summary.algorithm }}</strong>
                untuk semua tahun ({{ results.overall_summary.years_processed ? results.overall_summary.years_processed.join(', ') : 'Semua Tahun' }})
                - Mode Wide Format
              </span>
              <span v-else-if="singleResultData">
                Analisis menggunakan algoritma <strong>{{ singleResultData.algorithm }}</strong>
                {{ singleResultData.summary?.selectedYear ? `untuk tahun ${singleResultData.summary.selectedYear}` : '' }}
              </span>
            </p>
          </div>
        </div>
      </div>

      <div v-if="isLoading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>Memuat hasil analisis...</p>
      </div>

      <div v-if="error" class="error-container">
        <div class="alert alert-error">
          <h3>❌ Terjadi Kesalahan</h3>
          <p>{{ error }}</p>
          <button @click="$router.push('/upload')" class="btn btn-primary">
            🔄 Kembali ke Upload
          </button>
        </div>
      </div>

      <div v-if="results && !isLoading" class="results-section">
        
        <!-- Per Year Results -->
        <div v-if="results.clustering_type === 'per_year'">
          <YearlyResults :results="results" :sessionId="sessionId" />
        </div>
        
        <!-- All Years Wide Results -->
        <div v-else-if="results.clustering_type === 'all_years_wide'">
          <AllYearsResults :results="results" :sessionId="sessionId" />
        </div>
        
        <!-- Legacy Single Year Results (for backward compatibility) -->
        <div v-else-if="singleResultData" class="single-year-results">
          <div class="summary-cards">
            <div class="summary-card">
              <div class="card-icon">📊</div>
              <div class="card-content">
                <h3>{{ singleResultData.summary.total_regions }}</h3>
                <p>Total Daerah</p>
              </div>
            </div>
            
            <div class="summary-card">
              <div class="card-icon">🎯</div>
              <div class="card-content">
                <h3>{{ singleResultData.summary.num_clusters }}</h3>
                <p>Jumlah Cluster</p>
              </div>
            </div>
            
            <div class="summary-card">
              <div class="card-icon">⏱️</div>
              <div class="card-content">
                <h3>{{ singleResultData.summary.execution_time?.toFixed(2) }}s</h3>
                <p>Waktu Eksekusi</p>
              </div>
            </div>
            
            <div v-if="singleResultData.summary.iterations" class="summary-card">
              <div class="card-icon">🔄</div>
              <div class="card-content">
                <h3>{{ singleResultData.summary.iterations }}</h3>
                <p>Iterasi</p>
              </div>
            </div>
          </div>
          
          <div class="card">
            <h2>📈 Metrik Evaluasi</h2>
            <div class="evaluation-metrics">
              <div class="metric-card">
                <h3>Davies-Bouldin Index</h3>
                <div class="metric-value">
                  {{ (singleResultData.evaluation?.davies_bouldin !== undefined ? singleResultData.evaluation.davies_bouldin?.toFixed(4) : (singleResultData.summary?.davies_bouldin?.toFixed(4) || 'N/A')) || 'N/A' }}
                </div>
                <p class="metric-description">
                  Semakin rendah semakin baik. Mengukur rasio antara jarak dalam cluster dan antar cluster.
                </p>
              </div>
              
              <div class="metric-card">
                <h3>Silhouette Score</h3>
                <div class="metric-value">
                  {{ singleResultData.evaluation.silhouette_score?.toFixed(4) || 'N/A' }}
                </div>
                <p class="metric-description">
                  Rentang -1 hingga 1. Semakin tinggi semakin baik. Mengukur seberapa mirip objek dengan clusternya.
                </p>
              </div>
            </div>
          </div>

          <!-- Year filter - only show for regular single-year mode with multiple years -->
          <div v-if="results.clustering_type !== 'per_year' && results.clustering_type !== 'all_years_wide' && !singleResultData.summary?.selectedYear && availableYears.length > 1" class="card">
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

          <div class="visualizations">
            <ScatterPlot 
              :clusters="filteredClusters" 
              :title="`Scatter Plot - ${singleResultData.algorithm} Clustering`"
            />
            
            <BoxPlot 
              :clusters="filteredClusters" 
              :title="`Analisis Distribusi per Cluster - ${singleResultData.algorithm}`"
            />
            
            <CorrelationHeatmap 
              :clusters="filteredClusters" 
              :title="`Heatmap Korelasi Variabel - ${singleResultData.algorithm}`"
            />
            
            <InteractiveMap 
              :clusters="filteredClusters" 
              :title="`Peta Sebaran Cluster - ${singleResultData.algorithm}`"
            />
            
            <SilhouettePlot 
              :clusters="filteredClusters" 
              :title="`Silhouette Plot - ${singleResultData.algorithm}`"
              :silhouetteScore="singleResultData.evaluation.silhouette_score"
              :sessionId="sessionId"
            />
          </div>

          <!-- Use ClusterDetailCard component -->
          <ClusterDetailCard 
            :clusters="filteredClusters"
            :showMembership="singleResultData.algorithm === 'Fuzzy C-Means'"
          />

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
        </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, defineComponent } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ScatterPlot from '../components/ScatterPlot.vue'
import BoxPlot from '../components/BoxPlot.vue'
import CorrelationHeatmap from '../components/CorrelationHeatmap.vue'
import InteractiveMap from '../components/InteractiveMap.vue'
import YearlyResults from '../components/YearlyResults.vue'
import AllYearsResults from '../components/AllYearsResults.vue'
import ClusterDetailCard from '../components/ClusterDetailCard.vue'
import SilhouettePlot from '../components/SilhouettePlot.vue'
import apiService from '../services/apiService.js'

export default defineComponent({
  name: 'AnalysisEnhanced',
  components: {
    ScatterPlot,
    BoxPlot,
    CorrelationHeatmap,
    InteractiveMap,
    YearlyResults,
    AllYearsResults,
    ClusterDetailCard,
    SilhouettePlot
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const isLoading = ref(true)
    const error = ref('')
    const results = ref(null)
    const selectedYear = ref(null)
    const sessionId = ref(null)

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
    const singleResultData = computed(() => {
      if (!results.value) {
        return null;
      }
      
      const type = results.value.clustering_type;
      
      if (type === 'per_year') {
        return null; // Handled by YearlyResults component
      }
      
      if (type === 'all_years_wide') {
        // New 'all_years_wide' format
        return results.value.results_per_year?.all_years || null;
      }
      
      // Legacy "single year" format
      return results.value;
    });


    const availableYears = computed(() => {
      if (!results.value) return []
      
      // For per-year clustering, years are already available in overall_summary
      if (results.value.clustering_type === 'per_year') {
        return results.value.overall_summary?.years_processed || []
      }
      
      // UPDATED: Use singleResultData
      // For single year clustering, extract years from clusters
      // For all_years_wide, members won't have 'tahun', so this will correctly return []
      const clusters = singleResultData.value?.clusters;
      if (!clusters) return []
      
      const years = new Set()
      clusters.forEach(cluster => {
        cluster.members.forEach(member => {
          if (member.tahun) years.add(member.tahun)
        })
      })
      
      return Array.from(years).sort()
    })

    const filteredClusters = computed(() => {
      // UPDATED: Use singleResultData
      if (!singleResultData.value) return [] // Handles null, per_year, etc.
      
      const clusters = singleResultData.value.clusters
      if (!clusters) return []
      
      // No year filter active (this will be true for all_years_wide)
      if (!selectedYear.value) return clusters
      
      // Year filter is active (for legacy single-year)
      return clusters.map(cluster => ({
        ...cluster,
        members: cluster.members.filter(member => member.tahun === selectedYear.value),
        size: cluster.members.filter(member => member.tahun === selectedYear.value).length
      })).filter(cluster => cluster.size > 0)
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
        
        const sid = route.query.sessionId
        if (!sid) {
          throw new Error('Session ID tidak ditemukan')
        }
        
        sessionId.value = sid

        const rawResults = await apiService.getResults(sid)
        results.value = rawResults
        
        // The 'watch' on filteredClusters will handle setting the default selectedCluster
        
      } catch (err) {
        error.value = err.message || 'Gagal memuat hasil analisis'
      } finally {
        isLoading.value = false
      }
    }

    const exportToCSV = () => {
      // This is for legacy single year results only
      // Per year and all years have their own export in their components
      if (!singleResultData.value) {
        return;
      }
      
      const data = singleResultData.value;
      const csvData = []
      
      // Build headers
      let headers = ['Cluster', 'Kabupaten/Kota', 'Provinsi', 'Tahun', 'IPM', 'Garis Kemiskinan', 'Pengeluaran Per Kapita']
      
      if (data.algorithm === 'Fuzzy C-Means') {
        headers.push('Membership')
      }
      
      csvData.push(headers.join(','))
      
      // Use filteredClusters to respect the year filter (if any)
      filteredClusters.value.forEach(cluster => {
        cluster.members.forEach(member => {
          const row = [
            cluster.id,
            `"${member.kabupaten_kota}"`,
            `"${member.provinsi || 'N/A'}"`,
            member.tahun || 'N/A',
            member.ipm?.toFixed(2) || 'N/A',
            member.garis_kemiskinan || 'N/A',
            member.pengeluaran_per_kapita || 'N/A'
          ]
          
          if (data.algorithm === 'Fuzzy C-Means') {
            row.push((member.membership * 100).toFixed(2))
          }
          
          csvData.push(row.join(','))
        })
      })
      
      const blob = new Blob([csvData.join('\n')], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `clustering_results_${data.algorithm.toLowerCase()}_${Date.now()}.csv`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    }

    const exportToJSON = () => {
      // This is for legacy single year results only
      if (!singleResultData.value) return;
      
      const exportData = {
        ...singleResultData.value,
        clusters: filteredClusters.value,
        export_timestamp: new Date().toISOString()
      }

      const algorithmName = singleResultData.value?.algorithm || 'unknown';
      
      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `clustering_results_${algorithmName.toLowerCase()}_${Date.now()}.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    }


    const generateReport = () => {
      // This is for legacy single year results only
      if (!singleResultData.value) return
      
      const data = singleResultData.value;
      
      const reportLines = [
        `LAPORAN ANALISIS CLUSTERING`,
        `Algoritma: ${data.algorithm}`,
        `Mode: Single Year`,
        `Tanggal: ${new Date().toLocaleDateString('id-ID')}`,
        ``
      ]
      
      reportLines.push(`RINGKASAN:`)
      reportLines.push(`- Total Daerah: ${data.summary.total_regions}`)
      reportLines.push(`- Jumlah Cluster: ${data.summary.num_clusters}`)
      reportLines.push(`- Waktu Eksekusi: ${data.summary.execution_time?.toFixed(2)}s`)
      reportLines.push(``)
      reportLines.push(`EVALUASI:`)
      reportLines.push(`- Davies-Bouldin Index: ${data.evaluation.davies_bouldin?.toFixed(4) || 'N/A'}`)
      reportLines.push(`- Silhouette Score: ${data.evaluation.silhouette_score?.toFixed(4) || 'N/A'}`)
      reportLines.push(``)
      reportLines.push(`DETAIL CLUSTER:`)
      
      filteredClusters.value.forEach(cluster => {
        reportLines.push(``)
        reportLines.push(`Cluster ${cluster.id} (${cluster.size} daerah):`)
        if (cluster.centroid) {
          reportLines.push(`  Centroid:`)
          for (const [key, value] of Object.entries(cluster.centroid)) {
             reportLines.push(`    ${key}: ${value?.toFixed(2)}`)
          }
        }
        reportLines.push(`  Anggota:`)
        cluster.members.forEach(member => {
          reportLines.push(`    - ${member.kabupaten_kota} (${member.tahun || 'N/A'})`)
        })
      })
      
      const blob = new Blob([reportLines.join('\n')], { type: 'text/plain' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `clustering_report_${data.algorithm.toLowerCase()}_${Date.now()}.txt`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    }

    onMounted(() => {
      loadResults()
    })


    /**
     * Handles the PDF download request by constructing a payload for the API.
     * It correctly formats data for both 'per_year' and single analysis types.
     */
    const downloadPDFReport = async () => {
      if (!results.value) {
        error.value = 'No clustering results available to generate PDF.';
        return;
      }

      isLoading.value = true;
      error.value = '';
      
      try {
        let pdfPayload;

        if (results.value.clustering_type === 'per_year') {
          // For per-year results, the structure is already prepared.
          pdfPayload = {
            algorithm: results.value.overall_summary?.algorithm,
            yearly_results: results.value.results_per_year // Use 'results_per_year'
          };
        } else {
          // For single analysis (legacy or all_years_wide)
          const data = singleResultData.value; // Use our computed prop
          if (!data) throw new Error('Single result data is not available.');

          let yearKey;
          if (results.value.clustering_type === 'all_years_wide') {
            yearKey = 'all_years'; // Key from Python for wide format
          } else {
            // Legacy single year
            yearKey = data.summary?.selectedYear || availableYears.value[0] || 'all_years';
          }
          
          // FIX: Build 'data' from clusters, as 'data_with_clusters' doesn't exist
          const allMembers = data.clusters?.flatMap(c => 
            c.members.map(m => ({...m, cluster_id: c.id}))
          ) || [];
          
          pdfPayload = {
            algorithm: data.algorithm,
            yearly_results: {
              [yearKey]: {
                data: allMembers, // Use the constructed member list
                evaluation: data.evaluation || {},
                clusters: data.clusters || []
              }
            }
          };
        }
          
        if (!pdfPayload.algorithm || !pdfPayload.yearly_results) {
            throw new Error('Invalid data structure for PDF generation.');
        }

        // FIX: Moved hasData check to *after* pdfPayload is defined
        const hasData = Object.values(pdfPayload.yearly_results).some(
          yr => yr.clusters && yr.clusters.length > 0
        );
        if (!hasData) {
          throw new Error('Tidak ada data clustering untuk diekspor ke PDF.');
        }

        await apiService.downloadPDF({ clustering_results: pdfPayload });
        console.log('PDF generated successfully');

      } catch (err) {
        console.error('Error downloading PDF:', err);
        error.value = `Gagal mengunduh laporan PDF: ${err.message}`;
      } finally {
        isLoading.value = false;
      }
    };

    // Return all reactive values and methods
    return {
      isLoading,
      error,
      results,
      singleResultData,
      selectedYear,
      availableYears,
      filteredClusters,
      sessionId,
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
})
</script>

<style scoped>
/* Styles remain unchanged */
.analysis-page {
  padding: 2rem 0;
}

.page-header {
  margin-bottom: 3rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
  flex-wrap: wrap;
}

.page-header h1 {
  font-size: 2.5rem;
  color: #2d3748;
  margin-bottom: 1rem;
  text-align: left;
}

.page-header p {
  font-size: 1.2rem;
  color: #718096;
  text-align: left;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.header-actions .btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.header-actions .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.header-actions .btn .icon {
  font-size: 1.2rem;
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

/* Unified color theme - Purple gradient */
.summary-card,
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

.btn-success {
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important;
}

.btn-info {
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
}

.btn-warning {
  background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%) !important;
}

.cluster-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.quality-good {
  color: #48bb78;
  font-weight: 600;
}

.quality-fair {
  color: #ed8936;
  font-weight: 600;
}

.quality-poor {
  color: #f56565;
  font-weight: 600;
}

/* Consistent card styling */
.card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
  margin-bottom: 2rem;
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

/* Table header consistency */
thead th {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  padding: 1rem;
  text-align: left;
}

/* Membership bar color */
.membership-fill {
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}
</style>