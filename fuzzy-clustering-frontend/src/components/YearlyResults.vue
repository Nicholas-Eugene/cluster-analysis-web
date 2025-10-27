<template>
  <div class="yearly-results">
    <div class="results-header">
      <div class="header-content">
        <h2>📅 Hasil Clustering Per Tahun</h2>
        <p>Analisis clustering dilakukan secara terpisah untuk setiap tahun. Setiap tahun dianalisis secara independen menggunakan fitur: IPM, Garis Kemiskinan, dan Pengeluaran Per Kapita.</p>
        <div class="mode-note">
          <p><strong>💡 Catatan:</strong> Mode ini berbeda dengan "All Years" yang mengelompokkan berdasarkan pola multi-tahun. Hasil akan berbeda karena pendekatan analisisnya berbeda.</p>
        </div>
      </div>
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
            <div class="metric-header">
              <h5>Davies-Bouldin Index</h5>
            </div>
            <div class="metric-value">
              {{ results.overall_summary.average_evaluation.davies_bouldin?.toFixed(4) || 'N/A' }}
            </div>
          </div>
          <div class="metric-card">
            <div class="metric-header">
              <h5>Silhouette Score</h5>
            </div>
            <div class="metric-value">
              {{ results.overall_summary.average_evaluation.silhouette_score?.toFixed(4) || 'N/A' }}
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
                <div class="metric-header">
                  <h5>Davies-Bouldin Index</h5>
                </div>
                <div class="metric-value">
                  {{ selectedYearResults.evaluation.davies_bouldin?.toFixed(4) || 'N/A' }}
                </div>
              </div>
              <div class="metric-card">
                <div class="metric-header">
                  <h5>Silhouette Score</h5>
                </div>
                <div class="metric-value">
                  {{ selectedYearResults.evaluation.silhouette_score?.toFixed(4) || 'N/A' }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Visualizations for Selected Year -->
        <div v-if="selectedYearResults.clusters && selectedYearResults.clusters.length > 0" class="year-visualizations">
          <ScatterPlot 
            :clusters="selectedYearResults.clusters" 
            :title="`Scatter Plot - ${selectedYearResults.algorithm} Clustering (${selectedYear})`"
          />
          
          <BoxPlot 
            :clusters="selectedYearResults.clusters" 
            :title="`Analisis Distribusi - ${selectedYearResults.algorithm} (${selectedYear})`"
          />
          
          <CorrelationHeatmap 
            :clusters="selectedYearResults.clusters" 
            :title="`Heatmap Korelasi - ${selectedYearResults.algorithm} (${selectedYear})`"
          />
          
          <InteractiveMap 
            :clusters="selectedYearResults.clusters" 
            :title="`Peta Sebaran Cluster - ${selectedYearResults.algorithm} (${selectedYear})`"
          />
          
          <SilhouettePlot 
            :clusters="selectedYearResults.clusters" 
            :title="`Silhouette Plot - ${selectedYearResults.algorithm} (${selectedYear})`"
            :silhouetteScore="selectedYearResults.evaluation.silhouette_score"
            :sessionId="sessionId"
            :year="selectedYear"
          />
        </div>
        <div class="header-actions" style="margin-bottom: 2rem;">
          <button 
            @click="downloadPDF" 
            :disabled="isDownloadingPDF"
            class="btn btn-download"
          >
            <span v-if="!isDownloadingPDF">📄 Download PDF Report</span>
            <span v-else>⏳ Generating PDF...</span>
          </button>
        </div>
        <!-- Cluster Details for Selected Year -->
        <ClusterDetailCard 
          v-if="selectedYearResults.clusters && selectedYearResults.clusters.length > 0"
          :clusters="selectedYearResults.clusters"
          :showMembership="true"
        />
      </div>
    </div>
</template>

<script>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import ScatterPlot from './ScatterPlot.vue'
import BoxPlot from './BoxPlot.vue'
import CorrelationHeatmap from './CorrelationHeatmap.vue'
import InteractiveMap from './InteractiveMap.vue'
import SilhouettePlot from './SilhouettePlot.vue'
import ClusterDetailCard from './ClusterDetailCard.vue'
import { pdfService } from '../services/pdfService.js'

export default {
  name: 'YearlyResults',
  components: {
    ScatterPlot,
    BoxPlot,
    CorrelationHeatmap,
    InteractiveMap,
    SilhouettePlot,
    ClusterDetailCard
  },
  props: {
    results: {
      type: Object,
      required: true
    },
    sessionId: {
      type: String,
      required: false
    }
  },
  setup(props) {
    const selectedYear = ref(null)
    const selectedCluster = ref(null)

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
      if (!selectedCluster.value || !selectedYearResults.value?.clusters) return null
      return selectedYearResults.value.clusters.find(cluster => cluster.id === selectedCluster.value)
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

    const isDownloadingPDF = ref(false)

    const downloadPDF = async () => {
      if (!props.sessionId) {
        alert('Session ID tidak tersedia. Tidak dapat mendownload PDF.')
        return
      }

      isDownloadingPDF.value = true
      try {
        await pdfService.downloadAndSave(props.sessionId, 'yearly')
      } catch (error) {
        alert(error.message || 'Error generating PDF. Please try again.')
      } finally {
        isDownloadingPDF.value = false
      }
    }

    // Set default selected year when component mounts or data changes
    const setDefaultYear = async () => {
      await nextTick()
      try {
        if (availableYears.value && availableYears.value.length > 0 && !selectedYear.value) {
          selectedYear.value = availableYears.value[availableYears.value.length - 1] // Latest year
        }
      } catch (error) {
        // Ignore initialization errors
      }
    }

    onMounted(() => {
      setDefaultYear()
    })

    // Watch for data changes and reset selected year if needed
    watch(() => props.results, () => {
      setDefaultYear()
    }, { deep: true })

    return {
      selectedYear,
      availableYears,
      selectedYearResults,
      hasError,
      getClusterColor,
      formatCurrency,
      getDBIQuality,
      getDBIQualityText,
      getSilhouetteQuality,
      getSilhouetteQualityText,
      isDownloadingPDF,
      downloadPDF
    }
  }
}
</script>

<style scoped>
/* Based on AnalysisEnhanced.vue styling for consistency */
.yearly-results {
  padding: 2rem 0;
}

.results-header {
  margin-bottom: 3rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
}

.header-content {
  flex: 1;
  text-align: center;
}

.header-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.results-header h2 {
  font-size: 2.5rem;
  color: #2d3748;
  margin-bottom: 1rem;
}

.results-header p {
  font-size: 1.2rem;
  color: #718096;
  line-height: 1.6;
}

.mode-note {
  margin-top: 1rem;
  padding: 1rem;
  background: #f7fafc;
  border-left: 4px solid #667eea;
  border-radius: 4px;
}

.mode-note p {
  margin: 0;
  color: #4a5568;
  font-size: 0.9rem;
  line-height: 1.6;
}

.overall-summary {
  margin-bottom: 2rem;
}

.overall-summary h3 {
  color: #2d3748;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
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
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.summary-icon {
  font-size: 2rem;
  opacity: 0.9;
}

.summary-content h4 {
  color: white;
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
}

.summary-content p {
  color: rgba(255, 255, 255, 0.9);
  margin: 0.25rem 0 0 0;
  opacity: 0.9;
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

.metric-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.metric-card h5 {
  color: #2d3748;
  margin: 0;
  font-size: 1.25rem;
}

.metric-tooltip {
  position: relative;
  display: inline-block;
}

.tooltip-icon {
  cursor: help;
  font-size: 1rem;
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.tooltip-icon:hover {
  opacity: 1;
}

.tooltip-content {
  visibility: hidden;
  opacity: 0;
  position: absolute;
  z-index: 1000;
  bottom: 125%;
  left: 50%;
  transform: translateX(-50%);
  background-color: #2d3748;
  color: white;
  text-align: left;
  padding: 1rem;
  border-radius: 8px;
  min-width: 280px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: opacity 0.3s ease, visibility 0.3s ease;
}

.tooltip-content::after {
  content: "";
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: #2d3748 transparent transparent transparent;
}

.metric-tooltip:hover .tooltip-content {
  visibility: visible;
  opacity: 1;
}

.tooltip-content p {
  margin: 0 0 0.5rem 0;
  font-weight: 600;
  font-size: 0.9rem;
}

.tooltip-content ul {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0;
}

.tooltip-content li {
  padding: 0.25rem 0;
  font-size: 0.85rem;
  line-height: 1.4;
}

.tooltip-desc {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 0.8rem;
  opacity: 0.9;
  line-height: 1.4;
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

.year-selection {
  margin-bottom: 2rem;
}

.year-selector {
  margin-top: 1.5rem;
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
  gap: 1.5rem;
  margin-bottom: 2rem;
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

.visualizations {
  margin: 2rem 0;
}

/* Consistent card styling - Exact match with AnalysisEnhanced */
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

.card h2 {
  color: #2d3748;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.card h3 {
  color: #2d3748;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

/* Unified color theme - Purple gradient (from AnalysisEnhanced) */
.summary-item,
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

.btn-download {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  white-space: nowrap;
}

.btn-download:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.btn-download:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-download-main {
  font-size: 1.1rem;
  padding: 1rem 2rem;
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

.export-options {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1.5rem;
}

@media (max-width: 768px) {
  .yearly-results {
    padding: 1rem 0;
  }
  
  .results-header h2 {
    font-size: 2rem;
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

  .export-options {
    flex-direction: column;
  }
  
  .export-options button {
    width: 100%;
  }
}
</style>