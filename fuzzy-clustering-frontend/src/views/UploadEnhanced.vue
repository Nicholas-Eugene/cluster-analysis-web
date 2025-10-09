<template>
  <div class="upload-page">
    <div class="container">
      <div class="page-header">
        <h1>Analisis Clustering Regional Indonesia</h1>
        <p>Upload dataset dan konfigurasi parameter untuk analisis clustering <strong>per tahun</strong> menggunakan Fuzzy C-Means atau OPTICS</p>
        <div class="clustering-info">
          <div class="info-badge">
            <span class="info-icon">🗓️</span>
            <span>Clustering dilakukan terpisah untuk setiap tahun (2016-2024)</span>
          </div>
        </div>
      </div>

      <!-- Instructions Section -->
      <div class="card">
        <h2>📋 Petunjuk Dataset</h2>
        <div class="instructions">
          <div class="instruction-item">
            <h3>Format File</h3>
            <ul>
              <li>File harus berformat CSV (.csv) atau Excel (.xlsx)</li>
              <li>Untuk CSV: Encoding UTF-8 dengan delimiter koma (,)</li>
              <li>Baris pertama harus berisi header kolom</li>
              <li>Maksimal ukuran file: 10 MB</li>
            </ul>
          </div>
          
          <div class="instruction-item">
            <h3>Struktur Data yang Diperlukan</h3>
            <div class="data-structure">
              <table class="sample-table">
                <thead>
                  <tr>
                    <th>Kolom</th>
                    <th>Deskripsi</th>
                    <th>Contoh</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>kabupaten/kota</strong></td>
                    <td>Nama kabupaten/kota</td>
                    <td>Jakarta Pusat</td>
                  </tr>
                  <tr>
                    <td><strong>ipm_2016, ipm_2017, ..., ipm_2024</strong></td>
                    <td>Nilai IPM per tahun (2016-2024)</td>
                    <td>75.5, 76.2, 77.1, ...</td>
                  </tr>
                  <tr>
                    <td><strong>pengeluaran_2016, pengeluaran_2017, ..., pengeluaran_2024</strong></td>
                    <td>Pengeluaran per kapita per tahun (Rupiah)</td>
                    <td>8500000, 8700000, 8900000, ...</td>
                  </tr>
                  <tr>
                    <td><strong>garis_kemiskinan_2016, garis_kemiskinan_2017, ..., garis_kemiskinan_2024</strong></td>
                    <td>Garis kemiskinan per tahun (Rupiah)</td>
                    <td>532000, 548000, 565000, ...</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="instruction-item">
            <h3>Contoh Dataset</h3>
            <div class="sample-download">
              <p>Download template dataset untuk referensi:</p>
              <div class="download-buttons">
                <button @click="downloadSample" class="btn btn-secondary">
                  📥 Download Template CSV
                </button>
                <button @click="downloadExcelSample" class="btn btn-secondary">
                  📊 Download Template Excel
                </button>
                <button @click="loadSampleData" class="btn btn-info">
                  📂 Gunakan Data Sample
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- File Upload Section -->
      <div class="card">
        <h2>📤 Upload File Dataset</h2>
        <div class="upload-area">
          <div 
            class="file-upload"
            :class="{ 'dragover': isDragOver }"
            @dragover.prevent="isDragOver = true"
            @dragleave.prevent="isDragOver = false"
            @drop.prevent="handleFileDrop"
            @click="triggerFileInput"
          >
            <input 
              ref="fileInput"
              type="file"
              accept=".csv,.xlsx,.xls"
              @change="handleFileSelect"
              style="display: none"
            >
            
            <div v-if="!selectedFile" class="upload-placeholder">
              <div class="upload-icon">📁</div>
              <h3>Klik atau drag & drop file CSV atau Excel di sini</h3>
              <p>Format: .csv, .xlsx | Maksimal: 10 MB</p>
            </div>
            
            <div v-else class="file-info">
              <div class="file-icon">📄</div>
              <div class="file-details">
                <h3>{{ selectedFile.name }}</h3>
                <p>{{ formatFileSize(selectedFile.size) }}</p>
                <button @click.stop="removeFile" class="btn-remove">
                  ❌ Hapus File
                </button>
              </div>
            </div>
          </div>
          
          <div v-if="uploadError" class="alert alert-error">
            {{ uploadError }}
          </div>
          
          <div v-if="uploadSuccess" class="alert alert-success">
            {{ uploadSuccess }}
          </div>
        </div>
      </div>

      <!-- Data Preview Section -->
      <div v-if="dataPreview" class="card">
        <h2>👀 Preview Data</h2>
        <div class="data-preview">
          <div class="preview-stats">
            <div class="stat-item">
              <span class="stat-label">Total Baris:</span>
              <span class="stat-value">{{ dataPreview.totalRows }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Kolom:</span>
              <span class="stat-value">{{ dataPreview.columns.join(', ') }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Tahun Tersedia:</span>
              <span class="stat-value">{{ dataPreview.years.join(', ') }}</span>
            </div>
          </div>
          
          <div class="preview-table-container">
            <table class="preview-table">
              <thead>
                <tr>
                  <th v-for="column in dataPreview.columns" :key="column">
                    {{ column }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in dataPreview.sampleRows" :key="index">
                  <td v-for="column in dataPreview.columns" :key="column">
                    {{ row[column] }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Algorithm Selection -->
      <div class="card">
        <h2>🔬 Pilih Algoritma Clustering</h2>
        <div class="algorithm-selection">
          <div class="algorithm-grid">
            <div 
              class="algorithm-card"
              :class="{ active: selectedAlgorithm === 'fcm' }"
              @click="selectedAlgorithm = 'fcm'"
            >
              <h3>🌟 Fuzzy C-Means (FCM)</h3>
              <p>Algoritma clustering fuzzy yang memberikan tingkat keanggotaan untuk setiap data point ke dalam cluster.</p>
              <ul>
                <li>✅ Cocok untuk data dengan batas cluster yang tidak jelas</li>
                <li>✅ Memberikan tingkat keanggotaan (membership)</li>
                <li>✅ Stabil dan konsisten</li>
              </ul>
            </div>
            
            <div 
              class="algorithm-card"
              :class="{ active: selectedAlgorithm === 'optics' }"
              @click="selectedAlgorithm = 'optics'"
            >
              <h3>🔍 OPTICS</h3>
              <p>Algoritma clustering berbasis density yang dapat menemukan cluster dengan bentuk arbitrary dan menangani noise.</p>
              <ul>
                <li>✅ Dapat mendeteksi cluster dengan bentuk tidak beraturan</li>
                <li>✅ Menangani noise dan outlier</li>
                <li>✅ Tidak perlu menentukan jumlah cluster</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Parameters Configuration Section -->
      <div class="card">
        <h2>⚙️ Konfigurasi Parameter</h2>
        
        <!-- Year Selection -->
        <div class="form-group">
          <label class="form-label">
            Mode Analisis Clustering
            <span class="info-tooltip" title="Pilih tahun tertentu atau clustering per tahun">ℹ️</span>
          </label>
          <select v-model="parameters.selectedYear" class="form-select">
            <option value="">Clustering Per Tahun (Semua Tahun 2016-2024)</option>
            <option v-for="year in availableYears" :key="year" :value="year">
              Clustering Tahun {{ year }} Saja
            </option>
          </select>
          <div class="mode-explanation">
            <div v-if="!parameters.selectedYear" class="mode-info per-year">
              <span class="mode-icon">🗓️</span>
              <div class="mode-text">
                <strong>Mode Per Tahun:</strong> Clustering akan dilakukan secara terpisah untuk setiap tahun (2016-2024).
                Hasil akan menampilkan perbandingan clustering antar tahun.
              </div>
            </div>
            <div v-else class="mode-info single-year">
              <span class="mode-icon">🎯</span>
              <div class="mode-text">
                <strong>Mode Tahun Tunggal:</strong> Clustering hanya untuk tahun {{ parameters.selectedYear }}.
                Hasil akan fokus pada analisis tahun tersebut.
              </div>
            </div>
          </div>
        </div>

        <!-- FCM Parameters -->
        <div v-if="selectedAlgorithm === 'fcm'" class="parameters-form">
          <h3>Parameter Fuzzy C-Means</h3>
          <div class="grid grid-2">
            <div class="form-group">
              <label class="form-label">
                Jumlah Cluster (c)
                <span class="info-tooltip" title="Jumlah cluster yang diinginkan (2-10)">ℹ️</span>
              </label>
              <input 
                type="number" 
                v-model.number="parameters.numClusters"
                class="form-input"
                min="2"
                max="10"
                placeholder="Contoh: 3"
              >
              <small class="form-help">Rentang: 2-10 cluster</small>
            </div>

            <div class="form-group">
              <label class="form-label">
                Fuzzy Coefficient (m)
                <span class="info-tooltip" title="Parameter fuzziness yang mengontrol tingkat kekaburan cluster">ℹ️</span>
              </label>
              <input 
                type="number" 
                v-model.number="parameters.fuzzyCoeff"
                class="form-input"
                min="1.1"
                max="5"
                step="0.1"
                placeholder="Contoh: 2.0"
              >
              <small class="form-help">Rentang: 1.1-5.0 (default: 2.0)</small>
            </div>

            <div class="form-group">
              <label class="form-label">
                Maksimal Iterasi
                <span class="info-tooltip" title="Jumlah maksimal iterasi algoritma">ℹ️</span>
              </label>
              <input 
                type="number" 
                v-model.number="parameters.maxIter"
                class="form-input"
                min="50"
                max="1000"
                placeholder="Contoh: 300"
              >
              <small class="form-help">Rentang: 50-1000 iterasi</small>
            </div>

            <div class="form-group">
              <label class="form-label">
                Toleransi Error
                <span class="info-tooltip" title="Kriteria berhenti berdasarkan perubahan centroid">ℹ️</span>
              </label>
              <input 
                type="number" 
                v-model.number="parameters.tolerance"
                class="form-input"
                min="0.0001"
                max="0.1"
                step="0.0001"
                placeholder="Contoh: 0.0001"
              >
              <small class="form-help">Rentang: 0.0001-0.1</small>
            </div>
          </div>
        </div>

        <!-- OPTICS Parameters -->
        <div v-if="selectedAlgorithm === 'optics'" class="parameters-form">
          <h3>Parameter OPTICS</h3>
          <div class="grid grid-2">
            <div class="form-group">
              <label class="form-label">
                Minimum Samples
                <span class="info-tooltip" title="Jumlah minimum sampel dalam neighborhood">ℹ️</span>
              </label>
              <input 
                type="number" 
                v-model.number="parameters.minSamples"
                class="form-input"
                min="2"
                max="50"
                placeholder="Contoh: 5"
              >
              <small class="form-help">Rentang: 2-50 (default: 5)</small>
            </div>

            <div class="form-group">
              <label class="form-label">
                Xi Parameter
                <span class="info-tooltip" title="Minimum steepness pada reachability plot">ℹ️</span>
              </label>
              <input 
                type="number" 
                v-model.number="parameters.xi"
                class="form-input"
                min="0.01"
                max="1.0"
                step="0.01"
                placeholder="Contoh: 0.05"
              >
              <small class="form-help">Rentang: 0.01-1.0 (default: 0.05)</small>
            </div>

            <div class="form-group">
              <label class="form-label">
                Minimum Cluster Size
                <span class="info-tooltip" title="Ukuran minimum cluster sebagai fraksi dari data">ℹ️</span>
              </label>
              <input 
                type="number" 
                v-model.number="parameters.minClusterSize"
                class="form-input"
                min="0.01"
                max="0.5"
                step="0.01"
                placeholder="Contoh: 0.05"
              >
              <small class="form-help">Rentang: 0.01-0.5 (default: 0.05)</small>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="actions">
        <button 
          @click="validateAndProcess"
          :disabled="!canProcess || isProcessing"
          class="btn btn-lg btn-primary"
        >
          <span v-if="isProcessing" class="loading-spinner"></span>
          {{ isProcessing ? 'Memproses...' : `Mulai Clustering ${selectedAlgorithm.toUpperCase()}` }}
        </button>
        
        <button @click="resetForm" class="btn btn-secondary btn-lg">
          🔄 Reset Form
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import apiService from '../services/apiService.js'

export default {
  name: 'UploadEnhanced',
  setup() {
    const router = useRouter()
    const selectedFile = ref(null)
    const isDragOver = ref(false)
    const uploadError = ref('')
    const uploadSuccess = ref('')
    const isProcessing = ref(false)
    const dataPreview = ref(null)
    const fileInput = ref(null)
    const selectedAlgorithm = ref('fcm')

    const parameters = reactive({
      selectedYear: '',
      // FCM parameters
      numClusters: 3,
      fuzzyCoeff: 2.0,
      maxIter: 300,
      tolerance: 0.0001,
      // OPTICS parameters
      minSamples: 5,
      xi: 0.05,
      minClusterSize: 0.05
    })

    const availableYears = computed(() => {
      return Array.from({length: 10}, (_, i) => 2015 + i)
    })

    const canProcess = computed(() => {
      return selectedFile.value || dataPreview.value
    })

    const triggerFileInput = () => {
      fileInput.value.click()
    }

    const handleFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) {
        validateAndSetFile(file)
      }
    }

    const handleFileDrop = (event) => {
      isDragOver.value = false
      const file = event.dataTransfer.files[0]
      if (file) {
        validateAndSetFile(file)
      }
    }

    const validateAndSetFile = (file) => {
      uploadError.value = ''
      uploadSuccess.value = ''

      // Validate file type
      const fileName = file.name.toLowerCase()
      const validExtensions = ['.csv', '.xlsx', '.xls']
      const isValidType = validExtensions.some(ext => fileName.endsWith(ext))
      
      if (!isValidType) {
        uploadError.value = 'File harus berformat CSV (.csv) atau Excel (.xlsx, .xls)'
        return
      }

      // Validate file size (10MB)
      if (file.size > 10 * 1024 * 1024) {
        uploadError.value = 'Ukuran file tidak boleh lebih dari 10 MB'
        return
      }

      selectedFile.value = file
      uploadSuccess.value = 'File berhasil dipilih'
      
      // Parse file for preview
      if (fileName.endsWith('.csv')) {
        parseCSVPreview(file)
      } else {
        parseExcelPreview(file)
      }
    }

    const parseCSVPreview = (file) => {
      const reader = new FileReader()
      reader.onload = (e) => {
        try {
          const text = e.target.result
          const lines = text.split('\n').filter(line => line.trim())
          
          if (lines.length < 2) {
            uploadError.value = 'File CSV harus memiliki minimal 2 baris (header + data)'
            return
          }

          const headers = lines[0].split(',').map(h => h.trim())
          const sampleRows = lines.slice(1, 6).map(line => {
            const values = line.split(',').map(v => v.trim())
            const row = {}
            headers.forEach((header, index) => {
              row[header] = values[index] || ''
            })
            return row
          })

          // Extract years from data
          const years = [...new Set(lines.slice(1).map(line => {
            const values = line.split(',')
            const yearIndex = headers.indexOf('tahun')
            return yearIndex >= 0 ? values[yearIndex]?.trim() : null
          }).filter(year => year && !isNaN(year)))].sort()

          dataPreview.value = {
            totalRows: lines.length - 1,
            columns: headers,
            sampleRows: sampleRows,
            years: years
          }
        } catch (error) {
          uploadError.value = 'Gagal membaca file CSV. Pastikan format file benar.'
        }
      }
      reader.readAsText(file)
    }

    const parseExcelPreview = (file) => {
      // For Excel files, we'll show a basic preview without parsing
      // The actual parsing will be done on the backend
      const fileName = file.name
      
      // Create a mock preview for Excel files
      dataPreview.value = {
        totalRows: 'Unknown (akan diproses di server)',
        columns: ['kabupaten/kota', 'ipm_2016', 'pengeluaran_2016', 'garis_kemiskinan_2016', '...'],
        sampleRows: [
          {
            'kabupaten/kota': 'Akan ditampilkan setelah upload',
            'ipm_2016': '...',
            'pengeluaran_2016': '...',
            'garis_kemiskinan_2016': '...',
            '...': '...'
          }
        ],
        years: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
      }
      
      uploadSuccess.value = `File Excel ${fileName} berhasil dipilih. Preview lengkap akan tersedia setelah upload.`
    }

    const removeFile = () => {
      selectedFile.value = null
      dataPreview.value = null
      uploadError.value = ''
      uploadSuccess.value = ''
      fileInput.value.value = ''
    }

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    const downloadSample = () => {
      const sampleData = `kabupaten/kota,ipm_2016,pengeluaran_2016,garis_kemiskinan_2016,ipm_2017,pengeluaran_2017,garis_kemiskinan_2017,ipm_2018,pengeluaran_2018,garis_kemiskinan_2018,ipm_2019,pengeluaran_2019,garis_kemiskinan_2019,ipm_2020,pengeluaran_2020,garis_kemiskinan_2020,ipm_2021,pengeluaran_2021,garis_kemiskinan_2021,ipm_2022,pengeluaran_2022,garis_kemiskinan_2022,ipm_2023,pengeluaran_2023,garis_kemiskinan_2023,ipm_2024,pengeluaran_2024,garis_kemiskinan_2024
Jakarta Pusat,79.32,7800000,540000,79.78,8100000,560000,80.45,8400000,580000,81.12,8700000,600000,81.56,9000000,620000,82.12,9300000,640000,82.67,9600000,660000,83.23,9900000,680000,83.78,10200000,700000
Jakarta Utara,78.91,7200000,540000,79.45,7500000,560000,79.98,7800000,580000,80.52,8100000,600000,81.05,8400000,620000,81.58,8700000,640000,82.12,9000000,660000,82.65,9300000,680000,83.19,9600000,700000
Jakarta Barat,81.65,9200000,540000,82.23,9500000,560000,82.89,9800000,580000,83.56,10100000,600000,84.23,10400000,620000,84.89,10700000,640000,85.56,11000000,660000,86.23,11300000,680000,86.89,11600000,700000
Jakarta Selatan,79.88,6800000,540000,80.34,7100000,560000,80.78,7400000,580000,81.23,7700000,600000,81.67,8000000,620000,82.12,8300000,640000,82.56,8600000,660000,83.01,8900000,680000,83.45,9200000,700000
Jakarta Timur,78.23,6500000,420000,78.78,6800000,440000,79.34,7100000,460000,79.89,7400000,480000,80.45,7700000,500000,81.01,8000000,520000,81.56,8300000,540000,82.12,8600000,560000,82.67,8900000,580000
Surabaya,77.45,5800000,380000,77.89,6100000,400000,78.34,6400000,420000,78.78,6700000,440000,79.23,7000000,460000,79.67,7300000,480000,80.12,7600000,500000,80.56,7900000,520000,81.01,8200000,540000
Bandung,76.12,5200000,350000,76.67,5500000,370000,77.23,5800000,390000,77.78,6100000,410000,78.34,6400000,430000,78.89,6700000,450000,79.45,7000000,470000,80.01,7300000,490000,80.56,7600000,510000
Medan,75.89,4900000,340000,76.34,5200000,360000,76.78,5500000,380000,77.23,5800000,400000,77.67,6100000,420000,78.12,6400000,440000,78.56,6700000,460000,79.01,7000000,480000,79.45,7300000,500000
Semarang,74.56,4600000,320000,75.12,4900000,340000,75.67,5200000,360000,76.23,5500000,380000,76.78,5800000,400000,77.34,6100000,420000,77.89,6400000,440000,78.45,6700000,460000,79.01,7000000,480000
Palembang,73.78,4300000,310000,74.23,4600000,330000,74.78,4900000,350000,75.34,5200000,370000,75.89,5500000,390000,76.45,5800000,410000,77.01,6100000,430000,77.56,6400000,450000,78.12,6700000,470000`

      const blob = new Blob([sampleData], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'template_dataset_indonesia_wide.csv'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    }

    const downloadExcelSample = async () => {
      try {
        // Try to download the sample Excel file from backend
        const response = await fetch('/backend/sample_data_indonesia.xlsx')
        
        if (response.ok) {
          const blob = await response.blob()
          const url = window.URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = 'template_dataset_indonesia.xlsx'
          document.body.appendChild(a)
          a.click()
          document.body.removeChild(a)
          window.URL.revokeObjectURL(url)
        } else {
          throw new Error('File not found')
        }
      } catch (error) {
        // Fallback: show message to create Excel manually
        alert(`Template Excel tidak tersedia untuk download otomatis.
        
Silakan buat file Excel dengan struktur berikut:
- Kolom A: kabupaten/kota
- Kolom B-J: imp_2016, ipm_2017, ..., ipm_2024
- Kolom K-S: pengeluaran_2016, pengeluaran_2017, ..., pengeluaran_2024
- Kolom T-AB: garis_kemiskinan_2016, garis_kemiskinan_2017, ..., garis_kemiskinan_2024

Atau gunakan template CSV yang tersedia.`)
      }
    }

    const loadSampleData = async () => {
      try {
        // Load the sample data file from backend
        const response = await fetch('/backend/sample_data_indonesia_wide.csv')
        const text = await response.text()
        
        // Create a file object from the text
        const blob = new Blob([text], { type: 'text/csv' })
        const file = new File([blob], 'sample_data_indonesia_wide.csv', { type: 'text/csv' })
        
        validateAndSetFile(file)
        uploadSuccess.value = 'Data sample berhasil dimuat'
      } catch (error) {
        // Fallback to creating sample data directly
        const sampleData = `kabupaten/kota,ipm_2016,pengeluaran_2016,garis_kemiskinan_2016,ipm_2017,pengeluaran_2017,garis_kemiskinan_2017,ipm_2018,pengeluaran_2018,garis_kemiskinan_2018
Jakarta Pusat,79.32,7800000,540000,79.78,8100000,560000,80.45,8400000,580000
Jakarta Utara,78.91,7200000,540000,79.45,7500000,560000,79.98,7800000,580000
Surabaya,77.45,5800000,380000,77.89,6100000,400000,78.34,6400000,420000`
        
        const blob = new Blob([sampleData], { type: 'text/csv' })
        const file = new File([blob], 'sample_data_wide.csv', { type: 'text/csv' })
        
        validateAndSetFile(file)
        uploadSuccess.value = 'Data sample berhasil dimuat'
      }
    }

    const validateAndProcess = async () => {
      uploadError.value = ''
      
      if (!selectedFile.value) {
        uploadError.value = 'Silakan pilih file terlebih dahulu'
        return
      }

      // Validate parameters based on algorithm
      if (selectedAlgorithm.value === 'fcm') {
        if (parameters.numClusters < 2 || parameters.numClusters > 10) {
          uploadError.value = 'Jumlah cluster harus antara 2-10'
          return
        }

        if (parameters.fuzzyCoeff < 1.1 || parameters.fuzzyCoeff > 5) {
          uploadError.value = 'Fuzzy coefficient harus antara 1.1-5.0'
          return
        }
      } else if (selectedAlgorithm.value === 'optics') {
        if (parameters.minSamples < 2 || parameters.minSamples > 50) {
          uploadError.value = 'Minimum samples harus antara 2-50'
          return
        }

        if (parameters.xi < 0.01 || parameters.xi > 1.0) {
          uploadError.value = 'Xi parameter harus antara 0.01-1.0'
          return
        }
      }

      isProcessing.value = true
      
      try {
        const formData = new FormData()
        formData.append('file', selectedFile.value)
        formData.append('algorithm', selectedAlgorithm.value)
        
        if (parameters.selectedYear) {
          formData.append('selected_year', parameters.selectedYear)
        }

        // Add algorithm-specific parameters
        if (selectedAlgorithm.value === 'fcm') {
          formData.append('num_clusters', parameters.numClusters)
          formData.append('fuzzy_coeff', parameters.fuzzyCoeff)
          formData.append('max_iter', parameters.maxIter)
          formData.append('tolerance', parameters.tolerance)
        } else if (selectedAlgorithm.value === 'optics') {
          formData.append('min_samples', parameters.minSamples)
          formData.append('xi', parameters.xi)
          formData.append('min_cluster_size', parameters.minClusterSize)
        }

        const response = await apiService.uploadAndProcess(formData)
        
        uploadSuccess.value = 'Dataset berhasil diproses!'
        
        // Redirect to analysis page with results
        setTimeout(() => {
          router.push({
            name: 'AnalysisFull',
            query: { sessionId: response.session_id }
          })
        }, 1500)

      } catch (error) {
        uploadError.value = error.message || 'Terjadi kesalahan saat memproses data'
      } finally {
        isProcessing.value = false
      }
    }

    const resetForm = () => {
      removeFile()
      selectedAlgorithm.value = 'fcm'
      parameters.selectedYear = ''
      parameters.numClusters = 3
      parameters.fuzzyCoeff = 2.0
      parameters.maxIter = 300
      parameters.tolerance = 0.0001
      parameters.minSamples = 5
      parameters.xi = 0.05
      parameters.minClusterSize = 0.05
    }

    return {
      selectedFile,
      isDragOver,
      uploadError,
      uploadSuccess,
      isProcessing,
      dataPreview,
      fileInput,
      selectedAlgorithm,
      parameters,
      availableYears,
      canProcess,
      triggerFileInput,
      handleFileSelect,
      handleFileDrop,
      removeFile,
      formatFileSize,
      downloadSample,
      downloadExcelSample,
      loadSampleData,
      validateAndProcess,
      resetForm
    }
  }
}
</script>

<style scoped>
.upload-page {
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

.clustering-info {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
}

.info-badge {
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.info-icon {
  font-size: 1.2rem;
}

.mode-explanation {
  margin-top: 1rem;
}

.mode-info {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid;
}

.mode-info.per-year {
  background: #e6fffa;
  border-color: #38b2ac;
  color: #234e52;
}

.mode-info.single-year {
  background: #fef5e7;
  border-color: #ed8936;
  color: #744210;
}

.mode-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.mode-text {
  line-height: 1.5;
  font-size: 0.875rem;
}

.mode-text strong {
  display: block;
  margin-bottom: 0.25rem;
}

.instructions {
  display: grid;
  gap: 2rem;
}

.instruction-item h3 {
  color: #4a5568;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.instruction-item ul {
  color: #718096;
  padding-left: 1.5rem;
}

.instruction-item li {
  margin-bottom: 0.5rem;
  line-height: 1.6;
}

.sample-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.sample-table th,
.sample-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.sample-table th {
  background: #f7fafc;
  font-weight: 600;
  color: #4a5568;
}

.sample-table td {
  color: #718096;
}

.sample-download {
  background: #f7fafc;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
}

.sample-download p {
  margin-bottom: 1rem;
  color: #4a5568;
}

.download-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.download-buttons .btn {
  flex: 1;
  min-width: 150px;
}

.upload-area {
  margin-top: 2rem;
}

.file-upload {
  border: 3px dashed #cbd5e0;
  border-radius: 12px;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f7fafc;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.file-upload:hover,
.file-upload.dragover {
  border-color: #667eea;
  background: #edf2f7;
  transform: translateY(-2px);
}

.upload-placeholder {
  text-align: center;
}

.upload-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.6;
}

.upload-placeholder h3 {
  color: #4a5568;
  margin-bottom: 0.5rem;
  font-size: 1.25rem;
}

.upload-placeholder p {
  color: #718096;
  margin-bottom: 0.5rem;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  text-align: left;
}

.file-icon {
  font-size: 3rem;
}

.file-details h3 {
  color: #4a5568;
  margin-bottom: 0.5rem;
  font-size: 1.25rem;
}

.file-details p {
  color: #718096;
  margin-bottom: 1rem;
}

.btn-remove {
  background: #e53e3e;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-remove:hover {
  background: #c53030;
}

.data-preview {
  margin-top: 1rem;
}

.preview-stats {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.stat-item {
  background: #f7fafc;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.stat-label {
  font-weight: 600;
  color: #4a5568;
  margin-right: 0.5rem;
}

.stat-value {
  color: #667eea;
  font-weight: 600;
}

.preview-table-container {
  overflow-x: auto;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.preview-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.preview-table th,
.preview-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
  white-space: nowrap;
}

.preview-table th {
  background: #f7fafc;
  font-weight: 600;
  color: #4a5568;
  position: sticky;
  top: 0;
}

.preview-table td {
  color: #718096;
}

.algorithm-selection {
  margin-top: 2rem;
}

.algorithm-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 1rem;
}

.algorithm-card {
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.algorithm-card:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.algorithm-card.active {
  border-color: #667eea;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.algorithm-card h3 {
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.algorithm-card p {
  margin-bottom: 1rem;
  line-height: 1.6;
}

.algorithm-card ul {
  list-style: none;
  padding: 0;
}

.algorithm-card li {
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.parameters-form {
  margin-top: 2rem;
}

.parameters-form h3 {
  color: #4a5568;
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
}

.form-help {
  color: #718096;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
}

.info-tooltip {
  cursor: help;
  color: #667eea;
  margin-left: 0.5rem;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 3rem;
  flex-wrap: wrap;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
}

.btn-info {
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  color: white;
  margin-left: 1rem;
}

.btn-info:hover {
  background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%);
}

@media (max-width: 768px) {
  .upload-page {
    padding: 1rem 0;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .page-header p {
    font-size: 1rem;
  }
  
  .file-upload {
    padding: 2rem 1rem;
  }
  
  .file-info {
    flex-direction: column;
    text-align: center;
  }
  
  .preview-stats {
    flex-direction: column;
    gap: 1rem;
  }
  
  .algorithm-grid {
    grid-template-columns: 1fr;
  }
  
  .actions {
    flex-direction: column;
    align-items: center;
  }
  
  .btn-lg {
    width: 100%;
    max-width: 300px;
  }
}
</style>