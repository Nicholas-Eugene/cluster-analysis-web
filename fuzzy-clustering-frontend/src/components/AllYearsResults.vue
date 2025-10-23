<template>
  <div class="yearly-results">
    <!-- Results Header -->
    <div class="results-header">
      <div class="header-content">
        <h2>📊 Hasil Clustering All Years (Wide Format)</h2>
        <p>Analisis clustering menggunakan semua data tahun secara bersamaan. Setiap daerah direpresentasikan dengan semua nilai metrik dari berbagai tahun sebagai fitur (contoh: ipm_2015, ipm_2016, ..., ipm_2021).</p>
        <div class="mode-note">
          <p><strong>💡 Catatan:</strong> Mode "All Years" mengelompokkan daerah berdasarkan pola/tren mereka sepanjang waktu, sedangkan mode "Per Tahun" mengelompokkan daerah secara terpisah untuk setiap tahun. Hasil clustering berbeda karena pendekatan analisisnya berbeda.</p>
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
            <h4>{{ 
            (results.overall_summary.years_processed && Array.isArray(results.overall_summary.years_processed) && results.overall_summary.years_processed.length > 0)
              ? (results.overall_summary.years_processed.length > 3
                ? results.overall_summary.years_processed[0] + '-' + results.overall_summary.years_processed[results.overall_summary.years_processed.length - 1]
                : results.overall_summary.years_processed.join(', ')
              )
              : 'N/A' }}
            </h4>
            <p>Tahun yang Diproses</p>
          </div>
        </div>
        <div class="summary-item">
          <div class="summary-icon">📊</div>
          <div class="summary-content">
            <h4>{{ results.overall_summary.total_years || 0 }}</h4>
            <p>Total Tahun</p>
          </div>
        </div>
        <div class="summary-item">
          <div class="summary-icon">🎯</div>
          <div class="summary-content">
            <h4>{{ results.overall_summary.features_used ? results.overall_summary.features_used.length : 0 }}</h4>
            <p>Jumlah Fitur</p>
          </div>
        </div>
        <div class="summary-item">
          <div class="summary-content">
            <h4>{{ resultData.summary.total_regions }}</h4>
            <p>Total Daerah</p>
          </div>
        </div>
        <div class="summary-item">
          <div class="summary-content">
            <h4>{{ resultData.summary.num_clusters }}</h4>
            <p>Jumlah Cluster</p>
          </div>
        </div>
        <div class="summary-item">
          <div class="summary-content">
            <h4>{{ resultData.summary.execution_time?.toFixed(2) }}</h4>
            <p>Waktu Eksekusi</p>
          </div>
        </div>
        <div v-if="resultData.summary.iterations">
          <div class="summary-item">
          <div class="summary-icon">📈</div>
          <div class="summary-content">
            <h4>{{ resultData.summary.iterations }}</h4>
            <p>Iterasi</p>
          </div>
        </div>
        </div>
      </div>
    </div>

    <!-- Evaluation Metrics -->
    <div class="card">
      <h3>📈 Metrik Evaluasi</h3>
      <div class="year-evaluation">
        <div class="metrics-grid">
          <div class="metric-card">
            <div class="metric-header">
              <h5>Davies-Bouldin Index</h5>
              <div class="metric-tooltip">
                <span class="tooltip-icon">ℹ️</span>
                <div class="tooltip-content">
                  <p><strong>Rentang Nilai:</strong></p>
                  <ul>
                    <li>< 1.0 = Sangat Baik ✅</li>
                    <li>1.0 - 1.5 = Baik 👍</li>
                    <li>1.5 - 2.0 = Cukup ⚠️</li>
                    <li>> 2.0 = Perlu Perbaikan ❌</li>
                  </ul>
                  <p class="tooltip-desc">Semakin rendah semakin baik. Mengukur rasio jarak dalam cluster vs antar cluster.</p>
                </div>
              </div>
            </div>
            <div class="metric-value">
              {{ (resultData.evaluation?.davies_bouldin !== undefined ? resultData.evaluation.davies_bouldin?.toFixed(4) : (resultData.summary?.davies_bouldin?.toFixed(4) || 'N/A')) || 'N/A' }}
            </div>
          </div>
          
          <div class="metric-card">
            <div class="metric-header">
              <h5>Silhouette Score</h5>
              <div class="metric-tooltip">
                <span class="tooltip-icon">ℹ️</span>
                <div class="tooltip-content">
                  <p><strong>Rentang Nilai:</strong></p>
                  <ul>
                    <li>> 0.7 = Sangat Baik ✅</li>
                    <li>0.5 - 0.7 = Baik 👍</li>
                    <li>0.25 - 0.5 = Cukup ⚠️</li>
                    <li>< 0.25 = Perlu Perbaikan ❌</li>
                  </ul>
                  <p class="tooltip-desc">Rentang -1 hingga 1. Semakin tinggi semakin baik. Mengukur seberapa mirip objek dengan clusternya.</p>
                </div>
              </div>
            </div>
            <div class="metric-value">
              {{ resultData.evaluation.silhouette_score?.toFixed(4) || 'N/A' }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Visualizations -->
    <div class="year-visualizations">
      <div class="card viz-note">
        <h3>ℹ️ Catatan Visualisasi</h3>
        <p>
          Visualisasi berikut menggunakan <strong>nilai rata-rata</strong> dari semua tahun yang diproses 
          ({{ results.overall_summary.years_processed ? results.overall_summary.years_processed.join(', ') : 'N/A' }}).
          Clustering tetap menggunakan semua fitur multi-tahun untuk akurasi maksimal.
        </p>
      </div>
      
      <ScatterPlot 
        :clusters="resultData.clusters" 
        :title="`Scatter Plot - ${resultData.algorithm} Clustering (Rata-rata)`"
      />
      
      <BoxPlot 
        :clusters="resultData.clusters" 
        :title="`Analisis Distribusi per Cluster - ${resultData.algorithm} (Rata-rata)`"
      />
      
      <CorrelationHeatmap 
        :clusters="resultData.clusters" 
        :title="`Heatmap Korelasi Variabel - ${resultData.algorithm} (Rata-rata)`"
      />
      
      <InteractiveMap 
        :clusters="resultData.clusters" 
        :title="`Peta Sebaran Cluster - ${resultData.algorithm}`"
      />
      
      <SilhouettePlot 
        v-if="resultData.clusters && resultData.clusters.length > 0"
        :clusters="resultData.clusters" 
        :title="`Silhouette Plot - ${resultData.algorithm || 'Clustering'}`"
        :silhouetteScore="resultData.evaluation?.silhouette_score"
        :sessionId="sessionId"
      />

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
    </div>

    <!-- Cluster Details -->
    <ClusterDetailCard 
      :clusters="resultData.clusters"
      :showMembership="true"
    />

  </div>
</template>

<script>
import { computed, ref } from 'vue'
import ScatterPlot from './ScatterPlot.vue'
import BoxPlot from './BoxPlot.vue'
import CorrelationHeatmap from './CorrelationHeatmap.vue'
import InteractiveMap from './InteractiveMap.vue'
import ClusterDetailCard from './ClusterDetailCard.vue'
import SilhouettePlot from './SilhouettePlot.vue'
import { pdfService } from '../services/pdfService.js'

export default {
  name: 'AllYearsResults',
  components: {
    ScatterPlot,
    BoxPlot,
    CorrelationHeatmap,
    InteractiveMap,
    ClusterDetailCard,
    SilhouettePlot
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
    const resultData = computed(() => {
      return props.results.results_per_year?.all_years || null
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

    const isDownloadingPDF = ref(false)

    const downloadPDF = async () => {
      if (!props.sessionId) {
        alert('Session ID tidak tersedia. Tidak dapat mendownload PDF.')
        return
      }

      isDownloadingPDF.value = true
      try {
        await pdfService.downloadAndSave(props.sessionId, 'all_years')
      } catch (error) {
        alert(error.message || 'Error generating PDF. Please try again.')
      } finally {
        isDownloadingPDF.value = false
      }
    }

    return {
      resultData,
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
/* Based on YearlyResults.vue styling for consistency */
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

.year-summary {
  margin-bottom: 2rem;
}

.year-evaluation {
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.year-evaluation h4 {
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

.year-visualizations {
  margin: 2rem 0;
}

.viz-note {
  background: #f7fafc;
  border-left: 4px solid #667eea;
  margin-bottom: 2rem;
}

.viz-note h3 {
  color: #2d3748;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.viz-note p {
  color: #4a5568;
  line-height: 1.6;
  margin: 0;
}


/* Consistent card styling - Same as YearlyResults */
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

/* Unified color theme - Purple gradient */
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

@media (max-width: 768px) {
  .results-header {
    flex-direction: column;
  }
  
  .header-actions {
    width: 100%;
  }
  
  .btn-download {
    width: 100%;
  }
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
  
  .year-stats {
    grid-template-columns: 1fr;
  }
}</style>
