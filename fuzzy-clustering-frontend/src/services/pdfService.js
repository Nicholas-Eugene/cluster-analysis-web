/**
 * PDF Export Service
 * Handles PDF download from backend API
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

export const pdfService = {
  /**
   * Download PDF report from backend
   * @param {string} sessionId - Clustering session ID
   * @returns {Promise<Blob>} PDF file blob
   */
  async downloadPDF(sessionId) {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/clustering/download-pdf/${sessionId}/`,
        {
          responseType: 'blob',
          timeout: 120000, // 2 minutes timeout for PDF generation
        }
      )
      
      return response.data
    } catch (error) {
      throw new Error(
        error.response?.data?.error || 
        'Failed to download PDF report. Please try again.'
      )
    }
  },

  /**
   * Trigger PDF download in browser
   * @param {Blob} blob - PDF file blob
   * @param {string} filename - Desired filename
   */
  triggerDownload(blob, filename = 'clustering_report.pdf') {
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  },

  /**
   * Download and save PDF report
   * @param {string} sessionId - Clustering session ID
   * @param {string} mode - 'yearly' or 'all_years'
   */
  async downloadAndSave(sessionId, mode = 'yearly') {
    const timestamp = new Date().getTime()
    const filename = `clustering_report_${mode}_${timestamp}.pdf`
    
    const blob = await this.downloadPDF(sessionId)
    this.triggerDownload(blob, filename)
    
    return filename
  }
}

export default pdfService
