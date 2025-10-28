import axios from 'axios'

// Base URL relatif untuk Nginx proxy
const API_BASE_URL = '/api'; // Pastikan ini sudah benar

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  // headers: {
  //   'Content-Type': 'multipart/form-data', // Sebaiknya biarkan Axios atur ini saat mengirim FormData
  // },
});

// Request interceptor (Kode Anda sudah bagus)
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor (Kode Anda sudah bagus)
apiClient.interceptors.response.use(
  (response) => {
    // Anda mungkin ingin mengembalikan seluruh response agar bisa mengakses header (misalnya Content-Disposition)
    // return response.data; // Versi Anda
    return response; // Mengembalikan seluruh objek response
  },
  (error) => {
    let errorMessage = 'Terjadi kesalahan pada server'

    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response

      switch (status) {
        case 400:
          errorMessage = data.error || data.message || 'Data yang dikirim tidak valid' // Cek 'message' juga
          break
        case 401:
          errorMessage = 'Tidak memiliki akses (Unauthorized)'
          // Mungkin perlu redirect ke login di sini
          break
        case 403:
          errorMessage = 'Akses ditolak (Forbidden)'
          break
        case 404:
          errorMessage = 'Endpoint tidak ditemukan'
          break
        case 413:
          errorMessage = 'File terlalu besar'
          break
        case 422:
          errorMessage = data.error || data.message || 'Data tidak dapat diproses' // Cek 'message' juga
          break
        case 500:
          errorMessage = 'Terjadi kesalahan internal pada server'
          break
        default:
          errorMessage = data.error || data.message || `Error ${status}: ${error.message || 'Unknown server error'}`
      }
      // Log detail error ke konsol (opsional, berguna saat debugging)
      console.error('API Error Response:', error.response);
    } else if (error.request) {
      // Request made but no response received
      errorMessage = 'Tidak dapat terhubung ke server. Periksa koneksi internet Anda.'
      console.error('API No Response:', error.request);
    } else {
      // Something else happened in setting up the request
      errorMessage = error.message || 'Terjadi kesalahan tidak terduga saat menyiapkan request'
      console.error('API Request Setup Error:', error.message);
    }

    // Kembalikan error dengan pesan yang lebih jelas
    const enhancedError = new Error(errorMessage);
    enhancedError.originalError = error; // Simpan error asli jika perlu
    return Promise.reject(enhancedError);
  }
)

// API Service object
const apiService = {

  /**
   * Upload dataset file and process clustering
   * @param {FormData} formData - Form data containing file and parameters
   * @returns {Promise} Response with session ID and initial results
   */
  async uploadAndProcess(formData) {
    try {
      // Biarkan Axios mengatur Content-Type secara otomatis untuk FormData
      const response = await apiClient.post('/clustering/upload/', formData)
      return response.data; // Kembalikan hanya data dari response
    } catch (error) {
      console.error("Error during uploadAndProcess:", error.message || error);
      throw error // Lemparkan error yang sudah diproses oleh interceptor
    }
  },

  /**
   * Get clustering results by session ID
   * @param {string} sessionId - Session ID from upload response
   * @returns {Promise} Clustering results
   */
  async getResults(sessionId) {
    try {
      const response = await apiClient.get(`/clustering/results/${sessionId}/`)
      return response.data;
    } catch (error) {
      console.error("Error during getResults:", error.message || error);
      throw error
    }
  },

  /**
   * Get clustering status (for long-running operations)
   * @param {string} sessionId - Session ID
   * @returns {Promise} Status information
   */
  async getStatus(sessionId) {
    try {
      const response = await apiClient.get(`/clustering/status/${sessionId}/`)
      return response.data;
    } catch (error) {
      console.error("Error during getStatus:", error.message || error);
      throw error
    }
  },

  /**
   * Validate dataset format before upload
   * @param {File} file - CSV file to validate
   * @returns {Promise} Validation results
   */
  async validateDataset(file) {
    try {
      const formData = new FormData()
      formData.append('file', file)

      // Biarkan Axios mengatur Content-Type secara otomatis untuk FormData
      const response = await apiClient.post('/clustering/validate/', formData)
      return response.data;
    } catch (error) {
      console.error("Error during validateDataset:", error.message || error);
      throw error
    }
  },

  /**
   * Get available years from dataset
   * @param {string} sessionId - Session ID
   * @returns {Promise} Available years
   */
  async getAvailableYears(sessionId) {
    try {
      const response = await apiClient.get(`/clustering/years/${sessionId}/`)
      return response.data;
    } catch (error) {
      console.error("Error during getAvailableYears:", error.message || error);
      throw error
    }
  },

  /**
   * Re-run clustering with different parameters
   * @param {string} sessionId - Session ID
   * @param {Object} parameters - New clustering parameters
   * @returns {Promise} New clustering results
   */
  async rerunClustering(sessionId, parameters) {
    try {
      // Untuk mengirim JSON, set Content-Type ke application/json
      const response = await apiClient.post(`/clustering/rerun/${sessionId}/`, parameters, {
          headers: {
            'Content-Type': 'application/json'
          }
      })
      return response.data;
    } catch (error) {
      console.error("Error during rerunClustering:", error.message || error);
      throw error
    }
  },

  /**
   * Export clustering results in various formats
   * @param {string} sessionId - Session ID
   * @param {string} format - Export format ('csv', 'json', 'excel')
   * @returns {Promise} Export data or download URL/Blob
   */
  async exportResults(sessionId, format = 'csv') {
    try {
      const response = await apiClient.get(`/clustering/export/${sessionId}/?format=${format}`, {
        // Axios mengembalikan data blob jika responseType 'blob'
        responseType: format === 'excel' ? 'blob' : 'json'
      })
      // Interceptor sudah mengembalikan response utuh, jadi kita ambil datanya di sini
      return response.data;
    } catch (error) {
      console.error("Error during exportResults:", error.message || error);
      throw error
    }
  },

  /**
   * Get cluster analysis details
   * @param {string} sessionId - Session ID
   * @param {number} clusterId - Cluster ID
   * @returns {Promise} Detailed cluster analysis
   */
  async getClusterDetails(sessionId, clusterId) {
    try {
      const response = await apiClient.get(`/clustering/cluster/${sessionId}/${clusterId}/`)
      return response.data;
    } catch (error) {
      console.error("Error during getClusterDetails:", error.message || error);
      throw error
    }
  },

  /**
   * Get evaluation metrics details
   * @param {string} sessionId - Session ID
   * @returns {Promise} Detailed evaluation metrics
   */
  async getEvaluationMetrics(sessionId) {
    try {
      const response = await apiClient.get(`/clustering/evaluation/${sessionId}/`)
      return response.data;
    } catch (error) {
      console.error("Error during getEvaluationMetrics:", error.message || error);
      throw error
    }
  },

  /**
   * Generate comprehensive report
   * @param {string} sessionId - Session ID
   * @param {Object} options - Report options (e.g., { format: 'pdf' })
   * @returns {Promise} Report data or PDF blob
   */
  async generateReport(sessionId, options = {}) {
    try {
      const response = await apiClient.post(`/clustering/report/${sessionId}/`, options, {
        responseType: options.format === 'pdf' ? 'blob' : 'json',
        headers: {
            'Content-Type': 'application/json' // Opsi dikirim sebagai JSON
        }
      })
      return response.data; // Kembalikan data (bisa JSON atau Blob)
    } catch (error) {
      console.error("Error during generateReport:", error.message || error);
      throw error
    }
  },

  /**
   * Get geographical data for mapping
   * @param {string} sessionId - Session ID
   * @returns {Promise} Geographical coordinates and cluster assignments
   */
  async getGeographicalData(sessionId) {
    try {
      const response = await apiClient.get(`/clustering/geography/${sessionId}/`)
      return response.data;
    } catch (error) {
      console.error("Error during getGeographicalData:", error.message || error);
      throw error
    }
  },

  /**
   * Delete clustering session and associated data
   * @param {string} sessionId - Session ID
   * @returns {Promise} Deletion confirmation
   */
  async deleteSession(sessionId) {
    try {
      const response = await apiClient.delete(`/clustering/session/${sessionId}/`)
      return response.data;
    } catch (error) {
      console.error("Error during deleteSession:", error.message || error);
      throw error
    }
  },

  /**
   * Download clustering results as PDF (menggunakan endpoint baru)
   * @param {string} sessionId - Session ID dari hasil clustering
   * @returns {Promise} PDF blob for download
   */
  async downloadPDFNew(sessionId) { // Ganti nama agar tidak konflik dengan fungsi lama jika masih dipakai
     try {
       // Langsung GET ke endpoint backend yang menghasilkan PDF
       const response = await apiClient.get(`/clustering/download-pdf/${sessionId}/`, {
         responseType: 'blob', // Penting untuk unduhan file
       });

       // Interceptor sudah mengembalikan response utuh
       const blob = new Blob([response.data], { type: 'application/pdf' });

       // Cek jika response adalah JSON (error)
       if (response.headers['content-type'] && response.headers['content-type'].includes('application/json')) {
           const reader = new FileReader();
           const textResult = await new Promise((resolve, reject) => {
               reader.onload = () => resolve(reader.result);
               reader.onerror = reject;
               reader.readAsText(response.data); // Baca blob sebagai teks
           });
           const errorData = JSON.parse(textResult);
           throw new Error(errorData.error || errorData.message || 'Error generating PDF from server');
       }

       // Get filename from the Content-Disposition header or use default
       const contentDisposition = response.headers['content-disposition'];
       let filename = `clustering_report_${sessionId}.pdf`; // Nama file default yang lebih informatif
       if (contentDisposition) {
         const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
         if (filenameMatch && filenameMatch[1]) {
           filename = filenameMatch[1].replace(/['"]/g, '');
         }
       }

       // Create blob URL and trigger download
       const downloadUrl = window.URL.createObjectURL(blob);
       const link = document.createElement('a');
       link.href = downloadUrl;
       link.download = filename;
       document.body.appendChild(link);
       link.click();
       document.body.removeChild(link);
       window.URL.revokeObjectURL(downloadUrl);

       // Tidak mengembalikan apa-apa karena sudah trigger download
     } catch (error) {
        // Jika error berasal dari check JSON di atas
        if (error.message.includes('Error generating PDF from server')) {
             console.error("Error generating PDF:", error.message);
        }
        // Jika error dari Axios (sudah diproses interceptor)
        else {
            console.error("Error during downloadPDF:", error.message || error);
        }
       throw error; // Lemparkan error agar bisa ditangkap di komponen
     }
  },


  /**
   * Get demo results for showcase (when no real data uploaded)
   * @returns {Promise} Demo clustering results
   */
  async getDemoResults() {
    // Kode demo Anda sudah bagus
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          summary: { /* ... data demo ... */ },
          evaluation: { /* ... data demo ... */ },
          clusters: [ /* ... data demo ... */ ]
        })
      }, 1000) // Simulate API delay
    })
  }
}

export default apiService;