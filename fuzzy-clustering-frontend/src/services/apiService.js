import axios from 'axios'

// Base URL for Django backend API  
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout for clustering operations
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request interceptor
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

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    let errorMessage = 'Terjadi kesalahan pada server'
    
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response
      
      switch (status) {
        case 400:
          errorMessage = data.error || 'Data yang dikirim tidak valid'
          break
        case 401:
          errorMessage = 'Tidak memiliki akses'
          break
        case 403:
          errorMessage = 'Akses ditolak'
          break
        case 404:
          errorMessage = 'Endpoint tidak ditemukan'
          break
        case 413:
          errorMessage = 'File terlalu besar'
          break
        case 422:
          errorMessage = data.error || 'Data tidak dapat diproses'
          break
        case 500:
          errorMessage = 'Terjadi kesalahan pada server'
          break
        default:
          errorMessage = data.error || `Error ${status}: ${error.message}`
      }
    } else if (error.request) {
      // Request made but no response received
      errorMessage = 'Tidak dapat terhubung ke server. Periksa koneksi internet Anda.'
    } else {
      // Something else happened
      errorMessage = error.message || 'Terjadi kesalahan tidak terduga'
    }
    
    return Promise.reject(new Error(errorMessage))
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
      const response = await apiClient.post('/clustering/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      return response
    } catch (error) {
      throw error
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
      return response
    } catch (error) {
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
      return response
    } catch (error) {
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
      
      const response = await apiClient.post('/clustering/validate/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      return response
    } catch (error) {
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
      return response
    } catch (error) {
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
      const response = await apiClient.post(`/clustering/rerun/${sessionId}/`, parameters)
      return response
    } catch (error) {
      throw error
    }
  },

  /**
   * Export clustering results in various formats
   * @param {string} sessionId - Session ID
   * @param {string} format - Export format ('csv', 'json', 'excel')
   * @returns {Promise} Export data or download URL
   */
  async exportResults(sessionId, format = 'csv') {
    try {
      const response = await apiClient.get(`/clustering/export/${sessionId}/?format=${format}`, {
        responseType: format === 'excel' ? 'blob' : 'json'
      })
      return response
    } catch (error) {
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
      return response
    } catch (error) {
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
      return response
    } catch (error) {
      throw error
    }
  },

  /**
   * Generate comprehensive report
   * @param {string} sessionId - Session ID
   * @param {Object} options - Report options
   * @returns {Promise} Report data or PDF blob
   */
  async generateReport(sessionId, options = {}) {
    try {
      const response = await apiClient.post(`/clustering/report/${sessionId}/`, options, {
        responseType: options.format === 'pdf' ? 'blob' : 'json'
      })
      return response
    } catch (error) {
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
      return response
    } catch (error) {
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
      return response
    } catch (error) {
      throw error
    }
  },

  /**
   * Download clustering results as PDF
   * @param {Object} clusteringResults - Clustering results to include in PDF
   * @returns {Promise} PDF blob for download
   */
  async downloadPDF(clusteringResults) {
    try {
      // Format the data properly for the PDF generator
      const formattedData = {
        algorithm: clusteringResults.overall_summary?.algorithm || clusteringResults.algorithm || "Fuzzy C-Means",
        yearly_results: {}
      }
      if (clusteringResults.clustering_type === 'per_year') {
        // Process each year's data for per-year clustering
        for (const [year, yearData] of Object.entries(clusteringResults.results_per_year)) {
          if (!yearData.error) {
            formattedData.yearly_results[year] = {
              data: yearData.data_with_clusters,
              evaluation: {
                davies_bouldin: yearData.davies_bouldin_score,
                silhouette_score: yearData.silhouette_score
              },
              clusters: yearData.clusters.map(cluster => ({
                id: cluster.id,
                size: cluster.members ? cluster.members.length : 0,
                members: cluster.members || [],
                centroid: cluster.centroid || {}
              }))
            }
          }
        }
      } else {
        // Handle single-year clustering results
        const year = clusteringResults.summary?.selectedYear || new Date().getFullYear().toString()
        formattedData.yearly_results[year] = {
          data: clusteringResults.data_with_clusters || clusteringResults.data,
          evaluation: {
            davies_bouldin: clusteringResults.evaluation?.davies_bouldin,
            silhouette_score: clusteringResults.evaluation?.silhouette_score
          },
          clusters: (clusteringResults.clusters || []).map(cluster => ({
            id: cluster.id,
            size: cluster.members ? cluster.members.length : 0,
            members: cluster.members || [],
            centroid: cluster.centroid || {}
          }))
        }
      }
      
      const response = await axios.post(
        `${API_BASE_URL}/clustering/download-pdf/`,
        { clustering_results: formattedData },
        { 
          responseType: 'blob',
          headers: {
            'Accept': '*/*',
            'Content-Type': 'application/json'
          }
        }
      )

      // Check if the response is actually a PDF
      const contentType = response.headers['content-type']
      if (contentType && contentType.includes('application/json')) {
        // If we got JSON instead of PDF, it's probably an error
        const reader = new FileReader()
        const textResult = await new Promise((resolve) => {
          reader.onload = () => resolve(reader.result)
          reader.readAsText(response.data)
        })
        const errorData = JSON.parse(textResult)
        throw new Error(errorData.error || 'Error generating PDF')
      }

      // Get filename from the Content-Disposition header or use default
      const contentDisposition = response.headers['content-disposition']
      let filename = 'cluster_analysis_report.pdf'
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)
        if (filenameMatch && filenameMatch[1]) {
          filename = filenameMatch[1].replace(/['"]/g, '')
        }
      }

      // Create blob and trigger download
      const blob = new Blob([response.data], { type: 'application/pdf' })
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)
      
      return response
    } catch (error) {
      throw error
    }
  },

  /**
   * Get demo results for showcase (when no real data uploaded)
   * @returns {Promise} Demo clustering results
   */
  async getDemoResults() {
    // Return demo data for development/showcase purposes
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          summary: {
            total_regions: 34,
            num_clusters: 3,
            iterations: 42,
            execution_time: 2.34
          },
          evaluation: {
            davies_bouldin: 0.8234,
            silhouette_score: 0.6789
          },
          clusters: [
            {
              id: 0,
              centroid: {
                ipm: 81.5,
                garis_kemiskinan: 580000
              },
              members: [
                {
                  kabupaten_kota: 'Jakarta Pusat',
                  tahun: 2023,
                  ipm: 82.5,
                  garis_kemiskinan: 532000,
                  membership: 0.95
                },
                {
                  kabupaten_kota: 'Jakarta Selatan',
                  tahun: 2023,
                  ipm: 81.3,
                  garis_kemiskinan: 580000,
                  membership: 0.92
                },
                {
                  kabupaten_kota: 'Surabaya',
                  tahun: 2023,
                  ipm: 76.8,
                  garis_kemiskinan: 465000,
                  membership: 0.87
                }
              ]
            },
            {
              id: 1,
              centroid: {
                ipm: 74.2,
                garis_kemiskinan: 445000
              },
              members: [
                {
                  kabupaten_kota: 'Bandung',
                  tahun: 2023,
                  ipm: 75.2,
                  garis_kemiskinan: 485000,
                  membership: 0.89
                },
                {
                  kabupaten_kota: 'Semarang',
                  tahun: 2023,
                  ipm: 74.5,
                  garis_kemiskinan: 445000,
                  membership: 0.91
                },
                {
                  kabupaten_kota: 'Makassar',
                  tahun: 2023,
                  ipm: 73.2,
                  garis_kemiskinan: 380000,
                  membership: 0.85
                }
              ]
            },
            {
              id: 2,
              centroid: {
                ipm: 70.1,
                garis_kemiskinan: 380000
              },
              members: [
                {
                  kabupaten_kota: 'Medan',
                  tahun: 2023,
                  ipm: 72.1,
                  garis_kemiskinan: 420000,
                  membership: 0.88
                },
                {
                  kabupaten_kota: 'Palembang',
                  tahun: 2023,
                  ipm: 69.8,
                  garis_kemiskinan: 385000,
                  membership: 0.84
                },
                {
                  kabupaten_kota: 'Banjarmasin',
                  tahun: 2023,
                  ipm: 68.5,
                  garis_kemiskinan: 355000,
                  membership: 0.82
                }
              ]
            }
          ]
        })
      }, 1000) // Simulate API delay
    })
  }
}

export default apiService