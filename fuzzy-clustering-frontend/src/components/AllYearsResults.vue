<template>
  <div class="yearly-results">
    <!-- Results Header -->
    <div class="results-header">
      <h2>📅 Hasil Clustering All Years (Wide Format)</h2>
      <p>Analisis clustering menggunakan semua data tahun secara bersamaan. Setiap daerah direpresentasikan dengan semua nilai metrik dari berbagai tahun sebagai fitur (contoh: ipm_2015, ipm_2016, ..., ipm_2021).</p>
      <div class="mode-note">
        <p><strong>💡 Catatan:</strong> Mode "All Years" mengelompokkan daerah berdasarkan pola/tren mereka sepanjang waktu, sedangkan mode "Per Tahun" mengelompokkan daerah secara terpisah untuk setiap tahun. Hasil clustering berbeda karena pendekatan analisisnya berbeda.</p>
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
            <div class="metric-quality">
              <span class="quality-label">Kualitas:</span>
              <span :class="getDBIQuality(resultData.evaluation.davies_bouldin)">
                {{ getDBIQualityText(resultData.evaluation.davies_bouldin) }}
              </span>
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
            <div class="metric-quality">
              <span class="quality-label">Kualitas:</span>
              <span :class="getSilhouetteQuality(resultData.evaluation.silhouette_score)">
                {{ getSilhouetteQualityText(resultData.evaluation.silhouette_score) }}
              </span>
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
        :clusters="resultData.clusters" 
        :title="`Silhouette Plot - ${resultData.algorithm}`"
        :silhouetteScore="resultData.evaluation.silhouette_score"
      />
    </div>

    <!-- Cluster Details -->
    <ClusterDetailCard 
      :clusters="resultData.clusters"
      :showMembership="resultData.algorithm === 'Fuzzy C-Means'"
    />

    <!-- Export Options -->
    <div class="card year-cluster-details">
      <h3>📥 Export Hasil</h3>
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
</template>

<script>
import { computed } from 'vue'
import ScatterPlot from './ScatterPlot.vue'
import BoxPlot from './BoxPlot.vue'
import CorrelationHeatmap from './CorrelationHeatmap.vue'
import InteractiveMap from './InteractiveMap.vue'
import ClusterDetailCard from './ClusterDetailCard.vue'
import SilhouettePlot from './SilhouettePlot.vue'

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

    const exportToCSV = () => {
      const data = resultData.value
      const csvData = []
      
      // Build headers
      let headers = ['Cluster', 'Kabupaten/Kota', 'Provinsi', 'IPM', 'Garis Kemiskinan', 'Pengeluaran Per Kapita']
      
      if (data.algorithm === 'Fuzzy C-Means') {
        headers.push('Membership')
      }
      
      csvData.push(headers.join(','))
      
      // Add data rows
      data.clusters.forEach(cluster => {
        cluster.members.forEach(member => {
          const row = [
            cluster.id,
            `"${member.kabupaten_kota}"`,
            `"${member.provinsi || 'N/A'}"`,
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
      a.download = `clustering_results_${data.algorithm.toLowerCase()}_all_years_${Date.now()}.csv`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    }

    const exportToJSON = () => {
      const exportData = {
        ...props.results,
        export_timestamp: new Date().toISOString()
      }
      
      const algorithmName = resultData.value?.algorithm || 'unknown'
      
      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `clustering_results_${algorithmName.toLowerCase()}_all_years_${Date.now()}.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    }

    const generateReport = () => {
      const data = resultData.value
      
      const reportLines = [
        `LAPORAN ANALISIS CLUSTERING ALL YEARS`,
        `Algoritma: ${data.algorithm}`,
        `Mode: All Years (Wide Format)`,
        `Tanggal: ${new Date().toLocaleDateString('id-ID')}`,
        ``
      ]

      if (props.results.overall_summary) {
        reportLines.push(`INFORMASI CLUSTERING ALL YEARS:`)
        reportLines.push(`- Tahun yang Diproses: ${props.results.overall_summary.years_processed?.join(', ') || 'N/A'}`)
        reportLines.push(`- Total Tahun: ${props.results.overall_summary.total_years || 0}`)
        reportLines.push(`- Jumlah Fitur: ${props.results.overall_summary.features_used?.length || 0}`)
        reportLines.push(``)
      }
      
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
      
      data.clusters.forEach(cluster => {
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
          reportLines.push(`    - ${member.kabupaten_kota}`)
        })
      })
      
      const blob = new Blob([reportLines.join('\n')], { type: 'text/plain' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `clustering_report_${data.algorithm.toLowerCase()}_all_years_${Date.now()}.txt`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    }

    return {
      resultData,
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
/* Based on YearlyResults.vue styling for consistency */
.yearly-results {
  padding: 2rem 0;
}

.results-header {
  text-align: center;
  margin-bottom: 3rem;
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

.export-options {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1.5rem;
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
  
  .year-stats {
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
