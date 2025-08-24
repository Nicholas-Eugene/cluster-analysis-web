<template>
  <div class="upload-page">
    <div class="container">
      <div class="page-header">
        <h1>Unggah Dataset</h1>
        <p>Upload file dataset dan konfigurasi parameter untuk analisis clustering Fuzzy C-Means</p>
        <div class="mockup-notice">
          <strong>🎭 Mode Demo:</strong> Ini adalah versi mockup tanpa backend. Semua data menggunakan simulasi.
        </div>
      </div>

      <!-- Instructions Section -->
      <div class="card">
        <h2>📋 Petunjuk Dataset</h2>
        <div class="instructions">
          <div class="instruction-item">
            <h3>Format File</h3>
            <ul>
              <li>File harus berformat CSV (.csv)</li>
              <li>Encoding UTF-8 dengan delimiter koma (,)</li>
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
                    <td><strong>kabupaten_kota</strong></td>
                    <td>Nama kabupaten/kota</td>
                    <td>Jakarta Pusat</td>
                  </tr>
                  <tr>
                    <td><strong>tahun</strong></td>
                    <td>Tahun data</td>
                    <td>2023</td>
                  </tr>
                  <tr>
                    <td><strong>ipm</strong></td>
                    <td>Nilai Indeks Pembangunan Manusia</td>
                    <td>75.5</td>
                  </tr>
                  <tr>
                    <td><strong>garis_kemiskinan</strong></td>
                    <td>Nilai garis kemiskinan (Rupiah)</td>
                    <td>532000</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="instruction-item">
            <h3>Contoh Dataset</h3>
            <div class="sample-download">
              <p>Download template dataset untuk referensi:</p>
              <button @click="downloadSample" class="btn btn-secondary">
                📥 Download Template CSV
              </button>
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
              accept=".csv"
              @change="handleFileSelect"
              style="display: none"
            >
            
            <div v-if="!selectedFile" class="upload-placeholder">
              <div class="upload-icon">📁</div>
              <h3>Klik atau drag & drop file CSV di sini</h3>
              <p>Maksimal ukuran file: 10 MB</p>
              <small class="demo-note">(Mode demo - file apapun akan diterima)</small>
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

      <!-- Parameters Configuration Section -->
      <div class="card">
        <h2>⚙️ Konfigurasi Parameter Clustering</h2>
        <div class="parameters-form">
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

          <div class="form-group">
            <label class="form-label">
              Kolom Tahun (untuk analisis temporal)
              <span class="info-tooltip" title="Pilih tahun tertentu atau gunakan semua data">ℹ️</span>
            </label>
            <select v-model="parameters.selectedYear" class="form-select">
              <option value="">Semua Tahun</option>
              <option v-for="year in availableYears" :key="year" :value="year">
                {{ year }}
              </option>
            </select>
            <small class="form-help">Kosongkan untuk menggunakan semua data tahun</small>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="actions">
        <button 
          @click="validateAndProcess"
          :disabled="!selectedFile || isProcessing"
          class="btn btn-lg"
        >
          <span v-if="isProcessing" class="loading-spinner"></span>
          {{ isProcessing ? 'Memproses...' : 'Mulai Clustering (Demo)' }}
        </button>
        
        <button @click="resetForm" class="btn btn-secondary btn-lg">
          🔄 Reset Form
        </button>

        <button @click="loadDemoData" class="btn btn-warning btn-lg">
          🎭 Langsung ke Demo Hasil
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { mockData } from '../services/mockData.js'

export default {
  name: 'UploadMockup',
  setup() {
    const router = useRouter()
    const selectedFile = ref(null)
    const isDragOver = ref(false)
    const uploadError = ref('')
    const uploadSuccess = ref('')
    const isProcessing = ref(false)
    const dataPreview = ref(null)
    const fileInput = ref(null)

    const parameters = reactive({
      numClusters: 3,
      fuzzyCoeff: 2.0,
      maxIter: 300,
      tolerance: 0.0001,
      selectedYear: ''
    })

    const availableYears = computed(() => {
      return mockData.availableYears
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

      // Accept any file for demo
      selectedFile.value = file
      uploadSuccess.value = 'File berhasil dipilih (Mode Demo)'
      
      // Show mockup preview
      dataPreview.value = mockData.datasetPreview
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
      const sampleData = `kabupaten_kota,tahun,ipm,garis_kemiskinan
Jakarta Pusat,2023,82.5,532000
Jakarta Utara,2023,78.2,548000
Jakarta Barat,2023,79.1,525000
Jakarta Selatan,2023,81.3,580000
Jakarta Timur,2023,77.8,510000
Bandung,2023,75.2,485000
Surabaya,2023,76.8,465000
Medan,2023,72.1,420000
Semarang,2023,74.5,445000
Makassar,2023,73.2,380000`

      const blob = new Blob([sampleData], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'template_dataset_fcm.csv'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    }

    const validateAndProcess = async () => {
      uploadError.value = ''
      
      if (!selectedFile.value) {
        uploadError.value = 'Silakan pilih file terlebih dahulu'
        return
      }

      if (parameters.numClusters < 2 || parameters.numClusters > 10) {
        uploadError.value = 'Jumlah cluster harus antara 2-10'
        return
      }

      if (parameters.fuzzyCoeff < 1.1 || parameters.fuzzyCoeff > 5) {
        uploadError.value = 'Fuzzy coefficient harus antara 1.1-5.0'
        return
      }

      isProcessing.value = true
      
      try {
        // Simulate form data
        const formData = new FormData()
        formData.append('file', selectedFile.value)
        formData.append('num_clusters', parameters.numClusters)
        formData.append('fuzzy_coeff', parameters.fuzzyCoeff)
        formData.append('max_iter', parameters.maxIter)
        formData.append('tolerance', parameters.tolerance)
        if (parameters.selectedYear) {
          formData.append('selected_year', parameters.selectedYear)
        }

        // Simulate upload process without API call
        await new Promise(resolve => setTimeout(resolve, 1500))
        const response = { 
          session_id: 'mock-session-' + Date.now(),
          status: 'completed'
        }
        
        uploadSuccess.value = 'Dataset berhasil diproses! (Mode Demo)'
        
        // Redirect to analysis page with results
        setTimeout(() => {
          router.push({
            name: 'Analysis',
            query: { sessionId: response.session_id, demo: 'true' }
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
      parameters.numClusters = 3
      parameters.fuzzyCoeff = 2.0
      parameters.maxIter = 300
      parameters.tolerance = 0.0001
      parameters.selectedYear = ''
    }

    const loadDemoData = () => {
      router.push({
        name: 'Analysis',
        query: { demo: 'true' }
      })
    }

    return {
      selectedFile,
      isDragOver,
      uploadError,
      uploadSuccess,
      isProcessing,
      dataPreview,
      fileInput,
      parameters,
      availableYears,
      triggerFileInput,
      handleFileSelect,
      handleFileDrop,
      removeFile,
      formatFileSize,
      downloadSample,
      validateAndProcess,
      resetForm,
      loadDemoData
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

.mockup-notice {
  background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
  color: #2d3748;
  padding: 1rem 2rem;
  border-radius: 8px;
  margin-top: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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

.demo-note {
  color: #f6ad55;
  font-style: italic;
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

.parameters-form {
  margin-top: 2rem;
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