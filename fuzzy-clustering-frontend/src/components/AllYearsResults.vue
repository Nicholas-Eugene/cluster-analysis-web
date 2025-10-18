<template>
  <div class="all-years-results">
    <!-- Info Header -->
    <div class="card all-years-info">
      <h3>ℹ️ Informasi Clustering All Years (Wide Format)</h3>
      <p class="info-text">
        <strong>Mode clustering ini menggunakan semua data tahun secara bersamaan.</strong> Setiap daerah direpresentasikan 
        dengan semua nilai metrik dari berbagai tahun sebagai fitur (contoh: ipm_2015, ipm_2016, ..., ipm_2021).
      </p>
      <p class="info-text">
        ⚠️ <strong>Perbedaan dengan Mode Per Tahun:</strong> Mode "All Years" mengelompokkan daerah berdasarkan 
        <em>pola/tren mereka sepanjang waktu</em>, sedangkan mode "Per Tahun" mengelompokkan daerah secara terpisah 
        untuk setiap tahun. Hasil clustering berbeda karena kedua mode menjawab pertanyaan analisis yang berbeda.
      </p>
      <div class="info-details">
        <div class="info-item">
          <span class="info-label">Tahun yang Diproses:</span>
          <span class="info-value">{{ results.overall_summary.years_processed ? results.overall_summary.years_processed.join(', ') : 'N/A' }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">Total Tahun:</span>
          <span class="info-value">{{ results.overall_summary.total_years || 0 }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">Jumlah Fitur:</span>
          <span class="info-value">{{ results.overall_summary.features_used ? results.overall_summary.features_used.length : 0 }}</span>
        </div>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="summary-cards">
      <div class="summary-card">
        <div class="card-icon">📊</div>
        <div class="card-content">
          <h3>{{ resultData.summary.total_regions }}</h3>
          <p>Total Daerah</p>
        </div>
      </div>
      
      <div class="summary-card">
        <div class="card-icon">🎯</div>
        <div class="card-content">
          <h3>{{ resultData.summary.num_clusters }}</h3>
          <p>Jumlah Cluster</p>
        </div>
      </div>
      
      <div class="summary-card">
        <div class="card-icon">⏱️</div>
        <div class="card-content">
          <h3>{{ resultData.summary.execution_time?.toFixed(2) }}s</h3>
          <p>Waktu Eksekusi</p>
        </div>
      </div>
      
      <div v-if="resultData.summary.iterations" class="summary-card">
        <div class="card-icon">🔄</div>
        <div class="card-content">
          <h3>{{ resultData.summary.iterations }}</h3>
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
            {{ (resultData.evaluation?.davies_bouldin !== undefined ? resultData.evaluation.davies_bouldin?.toFixed(4) : (resultData.summary?.davies_bouldin?.toFixed(4) || 'N/A')) || 'N/A' }}
          </div>
          <p class="metric-description">
            Semakin rendah semakin baik. Mengukur rasio antara jarak dalam cluster dan antar cluster.
          </p>
          <div class="metric-quality">
            <span class="quality-label">Kualitas:</span>
            <span :class="getDBIQuality(resultData.evaluation.davies_bouldin)">
              {{ getDBIQualityText(resultData.evaluation.davies_bouldin) }}
            </span>
          </div>
        </div>
        
        <div class="metric-card">
          <h3>Silhouette Score</h3>
          <div class="metric-value">
            {{ resultData.evaluation.silhouette_score?.toFixed(4) || 'N/A' }}
          </div>
          <p class="metric-description">
            Rentang -1 hingga 1. Semakin tinggi semakin baik. Mengukur seberapa mirip objek dengan clusternya.
          </p>
          <div class="metric-quality">
            <span class="quality-label">Kualitas:</span>
            <span :class="getSilhouetteQuality(resultData.evaluation.silhouette_score)">
              {{ getSilhouetteQualityText(resultData.evaluation.silhouette_score) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Visualizations -->
    <div class="visualizations">
      <div class="card all-years-viz-note">
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
    </div>

    <!-- Cluster Details -->
    <ClusterDetailCard 
      :clusters="resultData.clusters"
      :showMembership="resultData.algorithm === 'Fuzzy C-Means'"
    />

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
</template>

<script>
import { computed } from 'vue'
import ScatterPlot from './ScatterPlot.vue'
import BoxPlot from './BoxPlot.vue'
import CorrelationHeatmap from './CorrelationHeatmap.vue'
import InteractiveMap from './InteractiveMap.vue'
import ClusterDetailCard from './ClusterDetailCard.vue'

export default {
  name: 'AllYearsResults',
  components: {
    ScatterPlot,
    BoxPlot,
    CorrelationHeatmap,
    InteractiveMap,
    ClusterDetailCard
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
/* Based on AnalysisEnhanced.vue styling for consistency */
.all-years-results {
  padding: 2rem 0;
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

.visualizations {
  margin: 2rem 0;
}

.all-years-info {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin-bottom: 2rem;
}

.all-years-info h3 {
  color: white;
  margin-bottom: 1rem;
}

.all-years-info .info-text {
  color: rgba(255, 255, 255, 0.95);
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.all-years-viz-note {
  background: #f7fafc;
  border-left: 4px solid #667eea;
  margin-bottom: 2rem;
}

.all-years-viz-note h3 {
  color: #2d3748;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.all-years-viz-note p {
  color: #4a5568;
  line-height: 1.6;
  margin: 0;
}

.info-details {
  display: grid;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 8px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
}

.info-label {
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.info-value {
  color: white;
  font-weight: 700;
}

.export-options {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1.5rem;
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

.card h2 {
  color: #2d3748;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

@media (max-width: 768px) {
  .all-years-results {
    padding: 1rem 0;
  }
  
  .summary-cards {
    grid-template-columns: 1fr;
  }
  
  .evaluation-metrics {
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
