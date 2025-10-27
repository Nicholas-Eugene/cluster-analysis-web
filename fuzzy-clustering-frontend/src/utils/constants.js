/**
 * Application Constants
 * Contains all constant values used throughout the frontend application
 */

// Cluster Colors - Consistent color scheme across all visualizations
export const CLUSTER_COLORS = [
  '#667eea', // Purple - Primary
  '#48bb78', // Green - Success
  '#ed8936', // Orange - Warning
  '#4299e1', // Blue - Info
  '#f56565', // Red - Danger
  '#38b2ac', // Teal
  '#9f7aea', // Purple Light
  '#ecc94b', // Yellow
  '#f687b3', // Pink
  '#4fd1c5', // Cyan
]

// Chart Default Configuration
export const CHART_DEFAULTS = {
  responsive: true,
  maintainAspectRatio: false,
  animation: {
    duration: 750,
    easing: 'easeInOutQuart'
  },
  plugins: {
    legend: {
      display: true,
      position: 'bottom',
      labels: {
        padding: 15,
        font: { size: 12 },
        usePointStyle: true
      }
    },
    tooltip: {
      enabled: true,
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      padding: 12,
      titleFont: { size: 14, weight: 'bold' },
      bodyFont: { size: 12 },
      cornerRadius: 8
    }
  }
}

// Metric Labels
export const METRIC_LABELS = {
  ipm: 'IPM',
  garis_kemiskinan: 'Garis Kemiskinan (Rp)',
  pengeluaran_per_kapita: 'Pengeluaran Per Kapita (Rp)'
}

// Metric Display Names for Charts
export const METRIC_DISPLAY_NAMES = {
  ipm: 'Indeks Pembangunan Manusia',
  garis_kemiskinan: 'Garis Kemiskinan',
  pengeluaran_per_kapita: 'Pengeluaran Per Kapita'
}

// Quality Thresholds for Metrics
export const QUALITY_THRESHOLDS = {
  davies_bouldin: {
    excellent: 1.0,
    good: 1.5,
    fair: 2.0
  },
  silhouette: {
    excellent: 0.7,
    good: 0.5,
    fair: 0.25
  }
}

// Quality CSS Classes
export const QUALITY_CLASSES = {
  excellent: 'quality-excellent',
  good: 'quality-good',
  fair: 'quality-fair',
  poor: 'quality-poor',
  unknown: 'quality-unknown'
}

// Noise Cluster IDs (for OPTICS)
export const NOISE_CLUSTER_IDS = [-1, '-1']

// Chart Heights
export const CHART_HEIGHTS = {
  small: 300,
  medium: 400,
  large: 600
}

// API Endpoints
export const API_BASE_URL = 'http://localhost:8000/api/clustering'

export const API_ENDPOINTS = {
  upload: '/upload',
  results: (sessionId) => `/results/${sessionId}`,
  export: (sessionId, format) => `/export/${sessionId}?format=${format}`,
  pdf: (sessionId) => `/pdf/${sessionId}`,
  geographical: (sessionId) => `/geographical/${sessionId}`,
  clusterDetails: (sessionId, clusterId) => `/cluster/${sessionId}/${clusterId}`,
  evaluation: (sessionId) => `/evaluation/${sessionId}`
}

// File Upload Configuration
export const FILE_UPLOAD = {
  maxSizeMB: 10,
  acceptedFormats: ['.csv', '.xlsx', '.xls'],
  acceptedMimeTypes: [
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  ]
}

// Algorithm Names
export const ALGORITHMS = {
  FCM: 'fcm',
  OPTICS: 'optics'
}

export const ALGORITHM_DISPLAY_NAMES = {
  fcm: 'Fuzzy C-Means',
  optics: 'OPTICS'
}

// Clustering Modes
export const CLUSTERING_MODES = {
  PER_YEAR: 'per_year',
  ALL_YEARS: 'all_years'
}

// Default Form Values
export const DEFAULT_FORM_VALUES = {
  algorithm: ALGORITHMS.FCM,
  numClusters: 3,
  fuzzyCoeff: 2.0,
  maxIter: 300,
  tolerance: 0.0001,
  minSamples: 5,
  xi: 0.05,
  minClusterSize: 0.05,
  clusteringMode: CLUSTERING_MODES.PER_YEAR
}

// Error Messages
export const ERROR_MESSAGES = {
  fileUpload: 'Gagal mengunggah file. Pastikan file dalam format yang benar.',
  noSession: 'Session ID tidak tersedia.',
  pdfGeneration: 'Gagal membuat PDF. Silakan coba lagi.',
  dataLoad: 'Gagal memuat data hasil clustering.',
  invalidFile: 'File tidak valid. Gunakan format CSV atau Excel (.xlsx).',
  fileTooLarge: 'Ukuran file terlalu besar. Maksimal 10MB.'
}

// Success Messages
export const SUCCESS_MESSAGES = {
  fileUpload: 'File berhasil diunggah dan diproses.',
  pdfDownload: 'PDF berhasil diunduh.',
  dataExport: 'Data berhasil diekspor.'
}
