<template>
  <div class="analysis-page">
    <div class="container">
      <div class="page-header">
        <h1>Analisis & Visualisasi</h1>
        <p>Dashboard hasil clustering Fuzzy C-Means untuk profil kemiskinan kabupaten/kota</p>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>Memuat hasil analisis...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>

      <!-- Results Section -->
      <div v-if="results && !isLoading" class="results-container">
        
        <!-- Summary Statistics -->
        <div class="card">
          <h2>📊 Ringkasan Hasil Clustering</h2>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">🏢</div>
              <div class="stat-content">
                <h3>{{ results.summary.total_regions }}</h3>
                <p>Total Kabupaten/Kota</p>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">🎯</div>
              <div class="stat-content">
                <h3>{{ results.summary.num_clusters }}</h3>
                <p>Jumlah Cluster</p>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">🔄</div>
              <div class="stat-content">
                <h3>{{ results.summary.iterations }}</h3>
                <p>Iterasi Konvergensi</p>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">⏱️</div>
              <div class="stat-content">
                <h3>{{ results.summary.execution_time }}s</h3>
                <p>Waktu Eksekusi</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Evaluation Metrics -->
        <div class="card">
          <h2>📈 Metrik Evaluasi Clustering</h2>
          <div class="metrics-grid">
            <div class="metric-card">
              <h3>Davies-Bouldin Index</h3>
              <div class="metric-value">{{ results.evaluation.davies_bouldin.toFixed(4) }}</div>
              <div class="metric-interpretation">
                <span class="metric-label">Interpretasi:</span>
                <span :class="getDBInterpretationClass(results.evaluation.davies_bouldin)">
                  {{ getDBInterpretation(results.evaluation.davies_bouldin) }}
                </span>
              </div>
              <p class="metric-description">
                Semakin rendah nilai DBI, semakin baik kualitas clustering
              </p>
            </div>
            
            <div class="metric-card">
              <h3>Silhouette Score</h3>
              <div class="metric-value">{{ results.evaluation.silhouette_score.toFixed(4) }}</div>
              <div class="metric-interpretation">
                <span class="metric-label">Interpretasi:</span>
                <span :class="getSilhouetteInterpretationClass(results.evaluation.silhouette_score)">
                  {{ getSilhouetteInterpretation(results.evaluation.silhouette_score) }}
                </span>
              </div>
              <p class="metric-description">
                Semakin tinggi nilai Silhouette Score, semakin baik pemisahan cluster
              </p>
            </div>
          </div>
        </div>

        <!-- Interactive Map -->
        <div class="card">
          <h2>🗺️ Peta Interaktif Hasil Clustering</h2>
          <div class="map-container">
            <div id="indonesia-map" class="map-view"></div>
            <div class="map-legend">
              <h4>Legend Cluster</h4>
              <div class="legend-items">
                <div 
                  v-for="(cluster, index) in results.clusters" 
                  :key="index"
                  class="legend-item"
                >
                  <div 
                    class="legend-color" 
                    :style="{ backgroundColor: getClusterColor(index) }"
                  ></div>
                  <span>Cluster {{ index + 1 }} ({{ cluster.members.length }} wilayah)</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Scatter Plot Visualization -->
        <div class="card">
          <h2>📈 Scatter Plot IPM vs Garis Kemiskinan</h2>
          <div class="chart-container">
            <canvas ref="scatterChart" class="chart-canvas"></canvas>
          </div>
          <div class="chart-controls">
            <div class="form-group">
              <label class="form-label">Filter Tahun:</label>
              <select v-model="selectedYear" @change="updateScatterPlot" class="form-select">
                <option value="">Semua Tahun</option>
                <option v-for="year in availableYears" :key="year" :value="year">
                  {{ year }}
                </option>
              </select>
            </div>
          </div>
        </div>

        <!-- Cluster Analysis -->
        <div class="card">
          <h2>🎯 Analisis Detail Cluster</h2>
          <div class="cluster-tabs">
            <button 
              v-for="(cluster, index) in results.clusters" 
              :key="index"
              @click="activeCluster = index"
              :class="['cluster-tab', { active: activeCluster === index }]"
              :style="{ borderColor: getClusterColor(index) }"
            >
              Cluster {{ index + 1 }}
            </button>
          </div>
          
          <div v-if="results.clusters[activeCluster]" class="cluster-details">
            <div class="cluster-info">
              <h3>Cluster {{ activeCluster + 1 }}</h3>
              <div class="cluster-stats">
                <div class="cluster-stat">
                  <span class="stat-label">Jumlah Anggota:</span>
                  <span class="stat-value">{{ results.clusters[activeCluster].members.length }}</span>
                </div>
                <div class="cluster-stat">
                  <span class="stat-label">Rata-rata IPM:</span>
                  <span class="stat-value">{{ results.clusters[activeCluster].centroid.ipm.toFixed(2) }}</span>
                </div>
                <div class="cluster-stat">
                  <span class="stat-label">Rata-rata Garis Kemiskinan:</span>
                  <span class="stat-value">Rp {{ formatCurrency(results.clusters[activeCluster].centroid.garis_kemiskinan) }}</span>
                </div>
              </div>
            </div>
            
            <div class="cluster-members">
              <h4>Anggota Cluster</h4>
              <div class="members-table-container">
                <table class="members-table">
                  <thead>
                    <tr>
                      <th>Kabupaten/Kota</th>
                      <th>Tahun</th>
                      <th>IPM</th>
                      <th>Garis Kemiskinan</th>
                      <th>Membership</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr 
                      v-for="member in results.clusters[activeCluster].members" 
                      :key="`${member.kabupaten_kota}-${member.tahun}`"
                    >
                      <td>{{ member.kabupaten_kota }}</td>
                      <td>{{ member.tahun }}</td>
                      <td>{{ member.ipm.toFixed(2) }}</td>
                      <td>Rp {{ formatCurrency(member.garis_kemiskinan) }}</td>
                      <td>
                        <div class="membership-bar">
                          <div 
                            class="membership-fill" 
                            :style="{ 
                              width: (member.membership * 100) + '%',
                              backgroundColor: getClusterColor(activeCluster)
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

        <!-- Cluster Characteristics -->
        <div class="card">
          <h2>📋 Karakteristik Cluster</h2>
          <div class="characteristics-grid">
            <div 
              v-for="(cluster, index) in results.clusters" 
              :key="index"
              class="characteristic-card"
              :style="{ borderLeftColor: getClusterColor(index) }"
            >
              <h3>Cluster {{ index + 1 }}</h3>
              <div class="characteristic-content">
                <div class="characteristic-item">
                  <strong>Profil Kemiskinan:</strong>
                  <span>{{ getClusterProfile(cluster) }}</span>
                </div>
                <div class="characteristic-item">
                  <strong>Rentang IPM:</strong>
                  <span>{{ getIPMRange(cluster) }}</span>
                </div>
                <div class="characteristic-item">
                  <strong>Rentang Garis Kemiskinan:</strong>
                  <span>{{ getPovertyLineRange(cluster) }}</span>
                </div>
                <div class="characteristic-item">
                  <strong>Wilayah Utama:</strong>
                  <span>{{ getMainRegions(cluster) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Export Options -->
        <div class="card">
          <h2>💾 Export Hasil</h2>
          <div class="export-options">
            <button @click="exportToCSV" class="btn btn-secondary">
              📄 Export CSV
            </button>
            <button @click="exportToJSON" class="btn btn-secondary">
              📋 Export JSON
            </button>
            <button @click="exportCharts" class="btn btn-secondary">
              📊 Export Charts (PNG)
            </button>
            <button @click="generateReport" class="btn">
              📖 Generate Report (PDF)
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import L from 'leaflet'
import apiService from '../services/apiService'

Chart.register(...registerables)

export default {
  name: 'Analysis',
  setup() {
    const isLoading = ref(true)
    const error = ref('')
    const results = ref(null)
    const activeCluster = ref(0)
    const selectedYear = ref('')
    const scatterChart = ref(null)
    const scatterChartInstance = ref(null)
    const map = ref(null)

    const availableYears = computed(() => {
      if (!results.value) return []
      const years = new Set()
      results.value.clusters.forEach(cluster => {
        cluster.members.forEach(member => {
          years.add(member.tahun)
        })
      })
      return Array.from(years).sort()
    })

    const clusterColors = [
      '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
      '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
    ]

    const getClusterColor = (index) => {
      return clusterColors[index % clusterColors.length]
    }

    const getDBInterpretation = (value) => {
      if (value < 1) return 'Sangat Baik'
      if (value < 1.5) return 'Baik'
      if (value < 2) return 'Sedang'
      return 'Perlu Perbaikan'
    }

    const getDBInterpretationClass = (value) => {
      if (value < 1) return 'interpretation-excellent'
      if (value < 1.5) return 'interpretation-good'
      if (value < 2) return 'interpretation-fair'
      return 'interpretation-poor'
    }

    const getSilhouetteInterpretation = (value) => {
      if (value > 0.7) return 'Sangat Baik'
      if (value > 0.5) return 'Baik'
      if (value > 0.25) return 'Sedang'
      if (value > 0) return 'Lemah'
      return 'Perlu Perbaikan'
    }

    const getSilhouetteInterpretationClass = (value) => {
      if (value > 0.7) return 'interpretation-excellent'
      if (value > 0.5) return 'interpretation-good'
      if (value > 0.25) return 'interpretation-fair'
      if (value > 0) return 'interpretation-weak'
      return 'interpretation-poor'
    }

    const formatCurrency = (value) => {
      return new Intl.NumberFormat('id-ID').format(value)
    }

    const getClusterProfile = (cluster) => {
      const avgIPM = cluster.centroid.ipm
      const avgPovertyLine = cluster.centroid.garis_kemiskinan

      if (avgIPM > 75 && avgPovertyLine > 500000) {
        return 'Pembangunan Tinggi, Biaya Hidup Tinggi'
      } else if (avgIPM > 75 && avgPovertyLine <= 500000) {
        return 'Pembangunan Tinggi, Biaya Hidup Rendah'
      } else if (avgIPM <= 75 && avgPovertyLine > 500000) {
        return 'Pembangunan Sedang, Biaya Hidup Tinggi'
      } else {
        return 'Pembangunan Sedang, Biaya Hidup Rendah'
      }
    }

    const getIPMRange = (cluster) => {
      const ipms = cluster.members.map(m => m.ipm)
      const min = Math.min(...ipms)
      const max = Math.max(...ipms)
      return `${min.toFixed(2)} - ${max.toFixed(2)}`
    }

    const getPovertyLineRange = (cluster) => {
      const lines = cluster.members.map(m => m.garis_kemiskinan)
      const min = Math.min(...lines)
      const max = Math.max(...lines)
      return `Rp ${formatCurrency(min)} - Rp ${formatCurrency(max)}`
    }

    const getMainRegions = (cluster) => {
      const regions = cluster.members.map(m => m.kabupaten_kota)
      const uniqueRegions = [...new Set(regions)]
      return uniqueRegions.slice(0, 3).join(', ') + 
             (uniqueRegions.length > 3 ? '...' : '')
    }

    const loadResults = async () => {
      try {
        isLoading.value = true
        
        // Check if we have session ID from upload
        const sessionId = route.query.sessionId
        if (sessionId) {
          results.value = await apiService.getResults(sessionId)
        } else {
          // Load demo data if no session
          results.value = await apiService.getDemoResults()
        }
        
        await nextTick()
        initializeVisualizations()
        
      } catch (err) {
        error.value = err.message || 'Gagal memuat hasil analisis'
      } finally {
        isLoading.value = false
      }
    }

    const initializeVisualizations = () => {
      initializeMap()
      createScatterPlot()
    }

    const initializeMap = () => {
      // Initialize Leaflet map
      map.value = L.map('indonesia-map').setView([-2.5, 118], 5)
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(map.value)

      // Add cluster markers (simplified for demo)
      if (results.value) {
        results.value.clusters.forEach((cluster, clusterIndex) => {
          cluster.members.forEach(member => {
            // Generate random coordinates for demo (in real app, use actual coordinates)
            const lat = -6 + (Math.random() * 12) // Indonesia latitude range
            const lng = 95 + (Math.random() * 46) // Indonesia longitude range
            
            const marker = L.circleMarker([lat, lng], {
              color: getClusterColor(clusterIndex),
              fillColor: getClusterColor(clusterIndex),
              fillOpacity: 0.7,
              radius: 8
            }).addTo(map.value)
            
            marker.bindPopup(`
              <strong>${member.kabupaten_kota}</strong><br>
              Cluster: ${clusterIndex + 1}<br>
              IPM: ${member.ipm.toFixed(2)}<br>
              Garis Kemiskinan: Rp ${formatCurrency(member.garis_kemiskinan)}
            `)
          })
        })
      }
    }

    const createScatterPlot = () => {
      if (!scatterChart.value || !results.value) return

      const ctx = scatterChart.value.getContext('2d')
      
      const datasets = results.value.clusters.map((cluster, index) => ({
        label: `Cluster ${index + 1}`,
        data: cluster.members
          .filter(member => !selectedYear.value || member.tahun == selectedYear.value)
          .map(member => ({
            x: member.garis_kemiskinan,
            y: member.ipm
          })),
        backgroundColor: getClusterColor(index),
        borderColor: getClusterColor(index),
        pointRadius: 6,
        pointHoverRadius: 8
      }))

      if (scatterChartInstance.value) {
        scatterChartInstance.value.destroy()
      }

      scatterChartInstance.value = new Chart(ctx, {
        type: 'scatter',
        data: { datasets },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Distribusi IPM vs Garis Kemiskinan per Cluster'
            },
            legend: {
              display: true,
              position: 'top'
            }
          },
          scales: {
            x: {
              title: {
                display: true,
                text: 'Garis Kemiskinan (Rupiah)'
              },
              ticks: {
                callback: function(value) {
                  return 'Rp ' + (value / 1000) + 'K'
                }
              }
            },
            y: {
              title: {
                display: true,
                text: 'Indeks Pembangunan Manusia (IPM)'
              },
              min: 60,
              max: 90
            }
          },
          interaction: {
            intersect: false
          }
        }
      })
    }

    const updateScatterPlot = () => {
      createScatterPlot()
    }

    const exportToCSV = () => {
      if (!results.value) return

      let csv = 'kabupaten_kota,tahun,ipm,garis_kemiskinan,cluster,membership\n'
      
      results.value.clusters.forEach((cluster, clusterIndex) => {
        cluster.members.forEach(member => {
          csv += `${member.kabupaten_kota},${member.tahun},${member.ipm},${member.garis_kemiskinan},${clusterIndex + 1},${member.membership}\n`
        })
      })

      const blob = new Blob([csv], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'clustering_results.csv'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    }

    const exportToJSON = () => {
      if (!results.value) return

      const jsonData = JSON.stringify(results.value, null, 2)
      const blob = new Blob([jsonData], { type: 'application/json' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'clustering_results.json'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    }

    const exportCharts = () => {
      if (scatterChartInstance.value) {
        const url = scatterChartInstance.value.toBase64Image()
        const a = document.createElement('a')
        a.href = url
        a.download = 'scatter_plot.png'
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
      }
    }

    const generateReport = () => {
      // This would generate a comprehensive PDF report
      alert('Fitur generate report PDF akan segera tersedia!')
    }

    onMounted(() => {
      loadResults()
    })

    return {
      isLoading,
      error,
      results,
      activeCluster,
      selectedYear,
      availableYears,
      scatterChart,
      getClusterColor,
      getDBInterpretation,
      getDBInterpretationClass,
      getSilhouetteInterpretation,
      getSilhouetteInterpretationClass,
      formatCurrency,
      getClusterProfile,
      getIPMRange,
      getPovertyLineRange,
      getMainRegions,
      updateScatterPlot,
      exportToCSV,
      exportToJSON,
      exportCharts,
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
  padding: 4rem 0;
}

.loading-container p {
  margin-top: 1rem;
  color: #718096;
  font-size: 1.1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.stat-card {
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  padding: 2rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  border-left: 4px solid #667eea;
}

.stat-icon {
  font-size: 3rem;
  opacity: 0.8;
}

.stat-content h3 {
  font-size: 2rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
}

.stat-content p {
  color: #718096;
  margin: 0;
  font-size: 1rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.metric-card {
  background: #f7fafc;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  border: 2px solid #e2e8f0;
}

.metric-card h3 {
  color: #4a5568;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.metric-value {
  font-size: 3rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 1rem;
}

.metric-interpretation {
  margin-bottom: 1rem;
}

.metric-label {
  font-weight: 600;
  color: #4a5568;
}

.interpretation-excellent { color: #38a169; }
.interpretation-good { color: #68d391; }
.interpretation-fair { color: #f6e05e; }
.interpretation-weak { color: #ed8936; }
.interpretation-poor { color: #e53e3e; }

.metric-description {
  color: #718096;
  font-size: 0.9rem;
  margin: 0;
}

.map-container {
  position: relative;
  margin-top: 2rem;
}

.map-view {
  height: 500px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.map-legend {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.map-legend h4 {
  margin: 0 0 1rem 0;
  color: #4a5568;
  font-size: 1rem;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 50%;
}

.chart-container {
  margin-top: 2rem;
  position: relative;
  height: 500px;
}

.chart-canvas {
  max-width: 100%;
  max-height: 100%;
}

.chart-controls {
  margin-top: 2rem;
  display: flex;
  gap: 2rem;
  align-items: center;
}

.cluster-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.cluster-tab {
  padding: 0.75rem 1.5rem;
  border: 2px solid #e2e8f0;
  border-bottom: 3px solid transparent;
  background: white;
  color: #4a5568;
  cursor: pointer;
  border-radius: 8px 8px 0 0;
  transition: all 0.3s ease;
  font-weight: 500;
}

.cluster-tab:hover,
.cluster-tab.active {
  background: #f7fafc;
  border-bottom-color: inherit;
}

.cluster-details {
  background: #f7fafc;
  padding: 2rem;
  border-radius: 0 8px 8px 8px;
}

.cluster-info {
  margin-bottom: 2rem;
}

.cluster-info h3 {
  color: #2d3748;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.cluster-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.cluster-stat {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  color: #4a5568;
  font-weight: 500;
}

.stat-value {
  color: #667eea;
  font-weight: 600;
}

.cluster-members h4 {
  color: #4a5568;
  margin-bottom: 1rem;
  font-size: 1.25rem;
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
  height: 24px;
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
  font-size: 0.8rem;
  font-weight: 600;
  color: #2d3748;
}

.characteristics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.characteristic-card {
  background: #f7fafc;
  padding: 2rem;
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.characteristic-card h3 {
  color: #2d3748;
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
}

.characteristic-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.characteristic-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.characteristic-item strong {
  color: #4a5568;
  font-size: 0.9rem;
}

.characteristic-item span {
  color: #718096;
}

.export-options {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .analysis-page {
    padding: 1rem 0;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .map-legend {
    position: relative;
    top: auto;
    right: auto;
    margin-top: 1rem;
  }
  
  .chart-controls {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .cluster-tabs {
    justify-content: center;
  }
  
  .cluster-stats {
    grid-template-columns: 1fr;
  }
  
  .export-options {
    flex-direction: column;
  }
}
</style>