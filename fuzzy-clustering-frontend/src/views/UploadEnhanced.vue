<template>
  <div class="upload-page">
    <div class="container">
      <div class="page-header">
        <h1>Analisis Clustering Regional Indonesia</h1>
        <p>Upload dataset dan konfigurasi parameter untuk analisis clustering <strong>per tahun</strong> menggunakan Fuzzy C-Means atau OPTICS</p>
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
            <p><strong>Gunakan format sederhana dengan 5 kolom:</strong></p>
            
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
                    <td><strong>tahun</strong></td>
                    <td>Tahun data</td>
                    <td>2016, 2017, 2018, ...</td>
                  </tr>
                  <tr>
                    <td><strong>ipm</strong></td>
                    <td>Nilai IPM</td>
                    <td>75.5</td>
                  </tr>
                  <tr>
                    <td><strong>garis_kemiskinan</strong></td>
                    <td>Garis kemiskinan (Rupiah)</td>
                    <td>532000</td>
                  </tr>
                  <tr>
                    <td><strong>pengeluaran_per_kapita</strong></td>
                    <td>Pengeluaran per kapita (Rupiah)</td>
                    <td>8500000</td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div class="format-note">
              <p><strong>Catatan Penting:</strong></p>
              <ul>
                <li>Setiap baris mewakili data satu kabupaten/kota untuk satu tahun</li>
                <li>Satu kabupaten/kota dapat memiliki beberapa baris untuk tahun yang berbeda</li>
                <li>Semua 5 kolom wajib ada dan tidak boleh kosong</li>
              </ul>
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

        <!-- Clustering Mode Dropdown -->
        <div class="form-group">
          <label class="form-label">Mode Clustering</label>
          <select v-model="clusteringMode" class="form-input">
            <option value="per_year">Per Tahun (default)</option>
            <option value="all_years">Semua Tahun Sekaligus</option>
          </select>
          <small class="form-help">Pilih apakah ingin clustering per tahun atau semua tahun sekaligus.</small>
        </div>

        <!-- Clustering Mode Info -->
        <div class="clustering-mode-info">
          <div v-if="clusteringMode === 'per_year'" class="mode-info per-year">
            <span class="mode-icon">🗓️</span>
            <div class="mode-text">
              <strong>Mode Clustering Per Tahun:</strong> Sistem akan melakukan clustering secara terpisah untuk setiap tahun yang tersedia dalam data.
              <br>
              <small>Contoh: Data 2016 akan di-cluster menjadi grup A,B,C - Data 2017 akan di-cluster menjadi grup A,B,C - dan seterusnya.</small>
              <br>
              <small class="mode-note-text"><strong>⚠️ Catatan:</strong> Hasil akan berbeda dengan mode "Semua Tahun" karena setiap tahun dianalisis secara independen.</small>
            </div>
          </div>
          <div v-else class="mode-info all-years">
            <span class="mode-icon">📅</span>
            <div class="mode-text">
              <strong>Mode Clustering Semua Tahun (Wide Format):</strong> Sistem akan menggabungkan semua data tahun menjadi satu baris per kabupaten/kota, dengan kolom berbeda untuk setiap tahun (misal: ipm_2016, ipm_2017, ...), lalu melakukan clustering satu kali pada data gabungan ini.
              <br>
              <small>Contoh: Data 2016-2021 akan digabung menjadi satu baris per kabupaten/kota dengan kolom ipm_2016, ipm_2017, ..., pengeluaran_per_kapita_2021, lalu di-cluster menjadi grup A,B,C berdasarkan pola/tren sepanjang waktu.</small>
              <br>
              <small class="mode-note-text"><strong>⚠️ Catatan:</strong> Hasil akan berbeda dengan mode "Per Tahun" karena clustering dilakukan berdasarkan pola multi-tahun, bukan per tahun terpisah.</small>
            </div>
          </div>
        </div>

        <!-- Year Selection (only for per_year mode) -->
        <div v-if="clusteringMode === 'per_year' && dataPreview && dataPreview.years && dataPreview.years.length > 0" class="form-group year-selection-group">
          <label class="form-label">
            <span class="label-icon">📅</span>
            Pilih Tahun untuk Di-cluster
          </label>
          <div class="year-selection-info">
            <p class="form-help">
              <strong>Wajib:</strong> Pilih minimal 1 tahun untuk mode "Per Tahun". 
              Gunakan "Pilih Semua" untuk memilih semua tahun atau centang tahun yang diinginkan.
            </p>
          </div>
          <div class="year-checkboxes">
            <label v-for="year in dataPreview.years" :key="year" class="year-checkbox-label">
              <input 
                type="checkbox" 
                :value="year" 
                v-model="selectedYears"
                class="year-checkbox"
              />
              <span class="checkbox-custom"></span>
              <span class="year-label">{{ year }}</span>
            </label>
            <div class="year-actions">
              <button type="button" @click="selectAllYears" class="btn-link">✓ Pilih Semua</button>
              <button type="button" @click="deselectAllYears" class="btn-link">✗ Hapus Semua</button>
            </div>
          </div>
          <div v-if="selectedYears.length > 0" class="selected-years-summary">
            <strong>✓ Tahun yang dipilih ({{ selectedYears.length }}):</strong> {{ selectedYears.sort().join(', ') }}
          </div>
          <div v-else class="selected-years-warning">
            <strong>⚠️ Peringatan:</strong> Belum ada tahun yang dipilih! Silakan pilih minimal 1 tahun.
          </div>
        </div>

        <!-- FCM Parameters -->
        <div v-if="selectedAlgorithm === 'fcm'" class="parameters-form">
          <h3>Parameter Fuzzy C-Means</h3>
          
          <div class="simple-params-note">
            <div class="note-icon">💡</div>
            <div class="note-text">
              <strong>Sederhana!</strong> Anda hanya perlu menentukan berapa jumlah kelompok (cluster) yang diinginkan. 
              Parameter teknis lainnya sudah diatur secara optimal oleh sistem.
            </div>
          </div>
          
          <div class="form-group form-group-featured">
            <label class="form-label">
              <span class="label-icon">🎯</span>
              Jumlah Cluster
              <span class="tooltip-container">
                <span class="info-icon">ℹ️</span>
                <div class="tooltip-content">
                  <strong>Apa itu Jumlah Cluster?</strong>
                  <p>Ini adalah jumlah kelompok yang ingin Anda buat dari data daerah. Misalnya:</p>
                  <ul>
                    <li><strong>3 cluster:</strong> Daerah akan dikelompokkan menjadi "Maju", "Sedang", dan "Berkembang"</li>
                    <li><strong>4 cluster:</strong> Daerah dikelompokkan menjadi 4 kategori berbeda</li>
                  </ul>
                  <p><strong>Tip:</strong> Mulai dengan 3-4 cluster untuk hasil yang mudah diinterpretasi.</p>
                </div>
              </span>
            </label>
            <input 
              type="number" 
              v-model.number="parameters.numClusters"
              class="form-input"
              min="2"
              max="10"
              placeholder="Contoh: 3"
            >
            <small class="form-help">
              <span class="help-icon">📌</span>
              Pilih antara 2-10 cluster. <strong>Rekomendasi: 3 atau 4 cluster</strong> untuk hasil yang mudah dipahami.
            </small>
          </div>
        </div>

        <!-- OPTICS Parameters -->
        <div v-if="selectedAlgorithm === 'optics'" class="parameters-form">
          <h3>Parameter OPTICS</h3>
          
          <div class="optics-intro-note">
            <div class="note-icon">🔍</div>
            <div class="note-text">
              <strong>OPTICS secara otomatis menemukan jumlah cluster yang optimal</strong> berdasarkan kepadatan data. 
              Anda perlu mengatur beberapa parameter untuk membantu algoritma memahami data Anda.
            </div>
          </div>
          
          <div class="grid grid-2">
            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">👥</span>
                Minimum Samples (Tetangga Minimum)
                <span class="tooltip-container">
                  <span class="info-icon">ℹ️</span>
                  <div class="tooltip-content">
                    <strong>Apa artinya?</strong>
                    <p>Jumlah minimum daerah yang harus berdekatan untuk membentuk satu kelompok.</p>
                    <strong>Penjelasan Sederhana:</strong>
                    <ul>
                      <li><strong>Nilai kecil (2-5):</strong> Lebih sensitif, bisa menemukan kelompok kecil</li>
                      <li><strong>Nilai sedang (5-10):</strong> Balanced, cocok untuk kebanyakan kasus</li>
                      <li><strong>Nilai besar (10-20):</strong> Hanya menemukan kelompok besar dan jelas</li>
                    </ul>
                    <p><strong>Tip:</strong> Gunakan 5 untuk data dengan puluhan daerah, 10-15 untuk data dengan ratusan daerah.</p>
                  </div>
                </span>
              </label>
              <input 
                type="number" 
                v-model.number="parameters.minSamples"
                class="form-input"
                min="2"
                max="50"
                placeholder="Contoh: 5"
              >
              <small class="form-help">
                <span class="help-icon">📌</span>
                Rekomendasi: <strong>5-10</strong> untuk hasil yang seimbang
              </small>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">📊</span>
                Xi Parameter (Kepekaan Pemisahan)
                <span class="tooltip-container">
                  <span class="info-icon">ℹ️</span>
                  <div class="tooltip-content">
                    <strong>Apa artinya?</strong>
                    <p>Parameter yang menentukan seberapa jelas perbedaan antar kelompok harus ada agar dianggap terpisah.</p>
                    <strong>Penjelasan Sederhana:</strong>
                    <ul>
                      <li><strong>Nilai kecil (0.01-0.03):</strong> Sangat sensitif, banyak cluster kecil</li>
                      <li><strong>Nilai sedang (0.05):</strong> Balanced, cocok untuk kebanyakan kasus ✓</li>
                      <li><strong>Nilai besar (0.1-0.2):</strong> Hanya menemukan perbedaan yang sangat jelas</li>
                    </ul>
                    <p><strong>Tip:</strong> Mulai dengan 0.05 (default), turunkan jika cluster terlalu sedikit, naikkan jika terlalu banyak.</p>
                  </div>
                </span>
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
              <small class="form-help">
                <span class="help-icon">📌</span>
                Rekomendasi: <strong>0.05</strong> (default, cocok untuk kebanyakan data)
              </small>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">📏</span>
                Minimum Cluster Size (Ukuran Cluster Minimum)
                <span class="tooltip-container">
                  <span class="info-icon">ℹ️</span>
                  <div class="tooltip-content">
                    <strong>Apa artinya?</strong>
                    <p>Persentase minimum dari total data yang harus ada dalam satu kelompok agar dianggap valid.</p>
                    <strong>Penjelasan Sederhana:</strong>
                    <ul>
                      <li><strong>0.05 (5%):</strong> Kelompok minimal berisi 5% dari total daerah</li>
                      <li><strong>0.10 (10%):</strong> Kelompok minimal berisi 10% dari total daerah</li>
                    </ul>
                    <strong>Contoh:</strong>
                    <p>Jika ada 100 daerah dan nilai 0.05, maka kelompok harus minimal berisi 5 daerah.</p>
                    <p><strong>Tip:</strong> Gunakan 0.05 untuk memperbolehkan kelompok kecil, atau 0.10 untuk hanya kelompok besar.</p>
                  </div>
                </span>
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
              <small class="form-help">
                <span class="help-icon">📌</span>
                Rekomendasi: <strong>0.05 (5%)</strong> untuk fleksibilitas yang baik
              </small>
            </div>
          </div>
          
          <div class="optics-summary">
            <div class="summary-header">💡 Panduan Cepat:</div>
            <div class="summary-grid">
              <div class="summary-item">
                <strong>Data Kecil (< 50 daerah):</strong>
                <span>Min Samples: 3-5 | Xi: 0.05 | Min Size: 0.05</span>
              </div>
              <div class="summary-item">
                <strong>Data Sedang (50-200 daerah):</strong>
                <span>Min Samples: 5-10 | Xi: 0.05 | Min Size: 0.05</span>
              </div>
              <div class="summary-item">
                <strong>Data Besar (> 200 daerah):</strong>
                <span>Min Samples: 10-15 | Xi: 0.05-0.10 | Min Size: 0.05</span>
              </div>
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
import { ref, reactive, computed, watch } from 'vue'
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
    // Clustering mode: 'per_year' or 'all_years'
    const clusteringMode = ref('per_year')
    // Selected years for per_year mode
    const selectedYears = ref([])

    const parameters = reactive({
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
          
          // Long format validation (5 columns)
          const requiredColumns = ['kabupaten/kota', 'tahun', 'ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita']
          const normalizedHeaders = headers.map(h => h.toLowerCase().replace(/[\/\s]/g, '_'))
          
          let validationError = null
          let years = []
          
          // Check for missing columns with flexible matching
          const missingColumns = []
          for (const requiredCol of requiredColumns) {
            const normalizedRequired = requiredCol.toLowerCase().replace(/[\/\s]/g, '_')
            const found = normalizedHeaders.some(h => {
              // Exact match or contains the key parts
              if (h === normalizedRequired) return true
              if (normalizedRequired.includes('kabupaten') && (h.includes('kabupaten') || h.includes('kota'))) return true
              if (normalizedRequired === 'pengeluaran_per_kapita' && (h.includes('pengeluaran') && h.includes('kapita'))) return true
              if (normalizedRequired === 'garis_kemiskinan' && h.includes('kemiskinan')) return true
              if (normalizedRequired === 'tahun' && h === 'tahun') return true
              if (normalizedRequired === 'ipm' && h === 'ipm') return true
              return false
            })
            if (!found) {
              missingColumns.push(requiredCol)
            }
          }
          
          if (missingColumns.length > 0) {
            validationError = `Kolom yang hilang: ${missingColumns.join(', ')}`
          } else {
            // Extract years from data
            const tahunIndex = headers.findIndex(h => h.toLowerCase() === 'tahun')
            if (tahunIndex >= 0) {
              years = [...new Set(lines.slice(1).map(line => {
                const values = line.split(',')
                return values[tahunIndex]?.trim()
              }).filter(year => year && !isNaN(year)))].sort()
            }
          }
          
          if (validationError) {
            uploadError.value = validationError
            uploadSuccess.value = ''
            return
          }

          const sampleRows = lines.slice(1, 6).map(line => {
            const values = line.split(',').map(v => v.trim())
            const row = {}
            headers.forEach((header, index) => {
              row[header] = values[index] || ''
            })
            return row
          })

          dataPreview.value = {
            totalRows: lines.length - 1,
            columns: headers,
            sampleRows: sampleRows,
            years: years,
            format: 'long'
          }
          
          // Auto-select all years for per_year mode
          if (clusteringMode.value === 'per_year' && years && years.length > 0) {
            selectedYears.value = [...years]
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
      
      // Create a mock preview for Excel files showing long format
      dataPreview.value = {
        totalRows: 'Unknown (akan diproses di server)',
        columns: ['kabupaten/kota', 'tahun', 'ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita'],
        sampleRows: [
          {
            'kabupaten/kota': 'Akan ditampilkan setelah upload',
            'tahun': '...',
            'ipm': '...',
            'garis_kemiskinan': '...',
            'pengeluaran_per_kapita': '...'
          }
        ],
        years: ['Akan dideteksi dari data'],
        format: 'long'
      }
      
      uploadSuccess.value = `File Excel ${fileName} berhasil dipilih. Format akan divalidasi saat upload.

Pastikan file menggunakan 5 kolom wajib:
- kabupaten/kota, tahun, ipm, garis_kemiskinan, pengeluaran_per_kapita`
    }

    const removeFile = () => {
      selectedFile.value = null
      dataPreview.value = null
      uploadError.value = ''
      uploadSuccess.value = ''
      selectedYears.value = []
      fileInput.value.value = ''
    }

    const selectAllYears = () => {
      if (dataPreview.value && dataPreview.value.years) {
        selectedYears.value = [...dataPreview.value.years]
      }
    }

    const deselectAllYears = () => {
      selectedYears.value = []
    }

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    const downloadSample = () => {
      const sampleData = `kabupaten/kota,tahun,ipm,garis_kemiskinan,pengeluaran_per_kapita
Jakarta Pusat,2016,79.32,540000,7800000
Jakarta Pusat,2017,79.78,560000,8100000
Jakarta Pusat,2018,80.45,580000,8400000
Jakarta Pusat,2019,81.12,600000,8700000
Jakarta Pusat,2020,81.56,620000,9000000
Jakarta Utara,2016,78.91,540000,7200000
Jakarta Utara,2017,79.45,560000,7500000
Jakarta Utara,2018,79.98,580000,7800000
Jakarta Utara,2019,80.52,600000,8100000
Jakarta Utara,2020,81.05,620000,8400000
Jakarta Barat,2016,81.65,540000,9200000
Jakarta Barat,2017,82.23,560000,9500000
Jakarta Barat,2018,82.89,580000,9800000
Jakarta Barat,2019,83.56,600000,10100000
Jakarta Barat,2020,84.23,620000,10400000
Surabaya,2016,77.45,380000,5800000
Surabaya,2017,77.89,400000,6100000
Surabaya,2018,78.34,420000,6400000
Surabaya,2019,78.78,440000,6700000
Surabaya,2020,79.23,460000,7000000
Bandung,2016,76.12,350000,5200000
Bandung,2017,76.67,370000,5500000
Bandung,2018,77.23,390000,5800000
Bandung,2019,77.78,410000,6100000
Bandung,2020,78.34,430000,6400000
Medan,2016,75.89,340000,4900000
Medan,2017,76.34,360000,5200000
Medan,2018,76.78,380000,5500000
Medan,2019,77.23,400000,5800000
Medan,2020,77.67,420000,6100000`

      const blob = new Blob([sampleData], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'template_dataset_indonesia_long.csv'
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
        const response = await fetch('/backend/sample_data_indonesia.csv')
        const text = await response.text()
        
        // Create a file object from the text
        const blob = new Blob([text], { type: 'text/csv' })
        const file = new File([blob], 'sample_data_indonesia.csv', { type: 'text/csv' })
        
        validateAndSetFile(file)
        uploadSuccess.value = 'Data sample berhasil dimuat'
      } catch (error) {
        // Fallback to creating sample data directly
        const sampleData = `kabupaten/kota,tahun,ipm,garis_kemiskinan,pengeluaran_per_kapita
Jakarta Pusat,2016,79.32,540000,7800000
Jakarta Pusat,2017,79.78,560000,8100000
Jakarta Pusat,2018,80.45,580000,8400000
Jakarta Utara,2016,78.91,540000,7200000
Jakarta Utara,2017,79.45,560000,7500000
Jakarta Utara,2018,79.98,580000,7800000
Surabaya,2016,77.45,380000,5800000
Surabaya,2017,77.89,400000,6100000
Surabaya,2018,78.34,420000,6400000`
        
        const blob = new Blob([sampleData], { type: 'text/csv' })
        const file = new File([blob], 'sample_data_long.csv', { type: 'text/csv' })
        
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

      // Validate year selection for per_year mode
      if (clusteringMode.value === 'per_year' && selectedYears.value.length === 0) {
        uploadError.value = '⚠️ Silakan pilih minimal 1 tahun untuk mode "Per Tahun". Gunakan tombol "Pilih Semua" atau centang tahun yang diinginkan.'
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
        formData.append('clustering_mode', clusteringMode.value)
        
        // Add selected years if any (for per_year mode)
        if (clusteringMode.value === 'per_year' && selectedYears.value.length > 0) {
          formData.append('selected_years', JSON.stringify(selectedYears.value))
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
            name: 'Analysis',
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
      parameters.numClusters = 3
      parameters.fuzzyCoeff = 2.0
      parameters.maxIter = 300
      parameters.tolerance = 0.0001
      parameters.minSamples = 5
      parameters.xi = 0.05
      parameters.minClusterSize = 0.05
      clusteringMode.value = 'per_year'
    }

    // Watch clustering mode changes and auto-select years for per_year mode
    watch(clusteringMode, (newMode) => {
      if (newMode === 'per_year' && dataPreview.value && dataPreview.value.years) {
        // Auto-select all available years when switching to per_year mode
        if (Array.isArray(dataPreview.value.years) && dataPreview.value.years.length > 0) {
          selectedYears.value = [...dataPreview.value.years]
        }
      } else if (newMode === 'all_years') {
        // Clear selection when switching to all_years mode
        selectedYears.value = []
      }
    })

    return {
      selectedFile,
      isDragOver,
      uploadError,
      uploadSuccess,
      isProcessing,
      dataPreview,
      fileInput,
      selectedAlgorithm,
      clusteringMode,
      selectedYears,
      parameters,
      canProcess,
      selectAllYears,
      deselectAllYears,
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
  gap: 1rem;
  flex-wrap: wrap;
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

.format-tabs {
  margin-top: 1rem;
}

.format-tabs h4 {
  color: #4a5568;
  margin: 2rem 0 1rem 0;
  font-size: 1.1rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.format-tabs h4:first-child {
  margin-top: 1rem;
}

.format-note {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #fff5f5;
  border-left: 4px solid #e53e3e;
  border-radius: 8px;
}

.format-note p {
  margin-bottom: 0.5rem;
  color: #742a2a;
  font-weight: 600;
}

.format-note ul {
  margin: 0;
  padding-left: 1.5rem;
  color: #742a2a;
}

.format-note li {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.format-note code {
  background: #fed7d7;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
}

.clustering-mode-info {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #e6fffa 0%, #f0fff4 100%);
  border-radius: 12px;
  border-left: 4px solid #38b2ac;
}

.clustering-mode-info .mode-info {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.clustering-mode-info .mode-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.clustering-mode-info .mode-text {
  line-height: 1.6;
  color: #234e52;
}

.clustering-mode-info .mode-text strong {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.clustering-mode-info .mode-text small {
  color: #2d5a5e;
  font-style: italic;
}

.clustering-mode-info .mode-text small.mode-note-text {
  display: block;
  margin-top: 0.5rem;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
  font-style: normal;
  color: #1a365d;
}

.year-selection-group {
  background: #f7fafc;
  border: 2px solid #667eea;
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}

.year-selection-info {
  margin-bottom: 1rem;
}

.year-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
  align-items: center;
}

.year-checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  user-select: none;
  font-weight: 500;
}

.year-checkbox-label:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);
}

.year-checkbox {
  display: none;
}

.checkbox-custom {
  width: 20px;
  height: 20px;
  border: 2px solid #cbd5e0;
  border-radius: 4px;
  display: inline-block;
  position: relative;
  transition: all 0.3s ease;
}

.year-checkbox:checked + .checkbox-custom {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
}

.year-checkbox:checked + .checkbox-custom::after {
  content: "✓";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-weight: bold;
  font-size: 14px;
}

.year-checkbox:checked ~ .year-label {
  color: #667eea;
  font-weight: 600;
}

.year-label {
  color: #4a5568;
  font-size: 1rem;
  transition: color 0.3s ease;
}

.year-actions {
  display: flex;
  gap: 1rem;
  margin-left: auto;
}

.btn-link {
  background: none;
  border: none;
  color: #667eea;
  font-weight: 600;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.btn-link:hover {
  background: #f7fafc;
  color: #764ba2;
}

.selected-years-summary {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  margin-top: 1rem;
  color: #2d3748;
  font-size: 0.95rem;
}

.selected-years-summary strong {
  color: #667eea;
}

.selected-years-warning {
  background: #fff3cd;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #ed8936;
  margin-top: 1rem;
  color: #975a16;
  font-size: 0.95rem;
  animation: pulse-warning 2s infinite;
}

.selected-years-warning strong {
  color: #c05621;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

@keyframes pulse-warning {
  0%, 100% {
    background-color: #fff3cd;
    border-color: #ed8936;
  }
  50% {
    background-color: #fef3c7;
    border-color: #f56565;
  }
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

/* FCM Simplified Parameters Styling */
.simple-params-note {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  background: linear-gradient(135deg, #e6f7ff 0%, #f0f9ff 100%);
  border-left: 4px solid #4299e1;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.simple-params-note .note-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.simple-params-note .note-text {
  line-height: 1.6;
  color: #2c5282;
}

.simple-params-note .note-text strong {
  color: #1e40af;
}

.form-group-featured {
  background: #f7fafc;
  padding: 2rem;
  border-radius: 12px;
  border: 2px solid #667eea;
  margin-bottom: 1.5rem;
}

.form-group-featured .form-input {
  font-size: 1.25rem;
  padding: 1rem;
  font-weight: 600;
  border: 2px solid #cbd5e0;
}

.form-group-featured .form-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.label-icon {
  font-size: 1.25rem;
  margin-right: 0.5rem;
}

.help-icon {
  margin-right: 0.5rem;
}

/* Tooltip Container */
.tooltip-container {
  position: relative;
  display: inline-block;
  margin-left: 0.5rem;
}

.tooltip-container .info-icon {
  cursor: help;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #667eea;
  color: white;
  font-size: 0.875rem;
  font-weight: 700;
  transition: all 0.3s ease;
}

.tooltip-container .info-icon:hover {
  background: #5a67d8;
  transform: scale(1.1);
}

.tooltip-content {
  visibility: hidden;
  opacity: 0;
  position: absolute;
  z-index: 1000;
  bottom: 125%;
  left: 50%;
  transform: translateX(-50%);
  min-width: 350px;
  max-width: 450px;
  background: white;
  color: #2d3748;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  transition: opacity 0.3s ease, visibility 0.3s ease;
  border: 2px solid #667eea;
}

.tooltip-content::after {
  content: "";
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -8px;
  border-width: 8px;
  border-style: solid;
  border-color: #667eea transparent transparent transparent;
}

.tooltip-container:hover .tooltip-content {
  visibility: visible;
  opacity: 1;
}

.tooltip-content strong {
  display: block;
  color: #667eea;
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
}

.tooltip-content p {
  margin: 0.75rem 0;
  line-height: 1.6;
}

.tooltip-content ul {
  margin: 0.75rem 0;
  padding-left: 1.5rem;
}

.tooltip-content li {
  margin: 0.5rem 0;
  line-height: 1.5;
}

/* Advanced Parameters Info */
.advanced-params-info {
  margin-top: 2rem;
  background: #f7fafc;
  border-radius: 8px;
  overflow: hidden;
}

.advanced-params-info details {
  cursor: pointer;
}

.advanced-params-info summary {
  padding: 1rem 1.5rem;
  background: #e2e8f0;
  font-weight: 600;
  color: #4a5568;
  user-select: none;
  transition: background 0.3s ease;
}

.advanced-params-info summary:hover {
  background: #cbd5e0;
}

.auto-params-list {
  padding: 1.5rem;
}

.auto-param-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  background: white;
  border-radius: 6px;
  margin-bottom: 0.5rem;
}

.auto-param-item .param-name {
  font-weight: 600;
  color: #4a5568;
}

.auto-param-item .param-value {
  color: #667eea;
  font-weight: 700;
}

.auto-params-note {
  margin-top: 1rem;
  padding: 1rem;
  background: #e6f7ff;
  border-left: 4px solid #4299e1;
  border-radius: 6px;
  color: #2c5282;
  font-style: italic;
}

/* OPTICS Styling */
.optics-intro-note {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  background: linear-gradient(135deg, #fef3c7 0%, #fef7cd 100%);
  border-left: 4px solid #f59e0b;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.optics-intro-note .note-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.optics-intro-note .note-text {
  line-height: 1.6;
  color: #78350f;
}

.optics-intro-note .note-text strong {
  color: #92400e;
}

.optics-summary {
  margin-top: 2rem;
  background: #f0fdf4;
  border: 2px solid #10b981;
  border-radius: 12px;
  padding: 1.5rem;
}

.optics-summary .summary-header {
  font-size: 1.1rem;
  font-weight: 700;
  color: #065f46;
  margin-bottom: 1rem;
}

.optics-summary .summary-grid {
  display: grid;
  gap: 1rem;
}

.optics-summary .summary-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  border-left: 4px solid #10b981;
}

.optics-summary .summary-item strong {
  color: #065f46;
  font-size: 1rem;
}

.optics-summary .summary-item span {
  color: #4a5568;
  font-size: 0.95rem;
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