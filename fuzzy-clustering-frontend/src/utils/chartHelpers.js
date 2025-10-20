/**
 * Chart Helper Functions
 * Reusable utilities for chart creation and configuration
 */

import { CLUSTER_COLORS, NOISE_CLUSTER_IDS, METRIC_LABELS } from './constants'

/**
 * Get cluster color by index
 * @param {number} index - Cluster index
 * @returns {string} Color hex code
 */
export const getClusterColor = (index) => {
  return CLUSTER_COLORS[index % CLUSTER_COLORS.length]
}

/**
 * Get cluster label with fallback handling
 * @param {Object} cluster - Cluster object
 * @returns {string} Cluster label
 */
export const getClusterLabel = (cluster) => {
  if (!cluster) return 'Unknown'
  
  // Handle noise clusters from OPTICS
  if (NOISE_CLUSTER_IDS.includes(cluster.id)) {
    return 'Noise (Outliers)'
  }
  
  // Return interpretation label if available
  if (cluster.interpretation?.label) {
    return String(cluster.interpretation.label)
  }
  
  return `Cluster ${cluster.id}`
}

/**
 * Check if cluster is a noise cluster
 * @param {Object} cluster - Cluster object
 * @returns {boolean} True if noise cluster
 */
export const isNoiseCluster = (cluster) => {
  return NOISE_CLUSTER_IDS.includes(cluster.id)
}

/**
 * Format metric label for display
 * @param {string} metric - Metric key
 * @returns {string} Formatted label
 */
export const formatMetricLabel = (metric) => {
  return METRIC_LABELS[metric] || metric
}

/**
 * Format currency value
 * @param {number} value - Value to format
 * @returns {string} Formatted currency string
 */
export const formatCurrency = (value) => {
  if (!value && value !== 0) return 'N/A'
  
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0
  }).format(value)
}

/**
 * Format number with thousand separators
 * @param {number} value - Value to format
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted number string
 */
export const formatNumber = (value, decimals = 2) => {
  if (!value && value !== 0) return 'N/A'
  
  return new Intl.NumberFormat('id-ID', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(value)
}

/**
 * Validate canvas and context
 * @param {Object} canvasRef - Canvas reference
 * @returns {Object|null} Context or null if invalid
 */
export const getValidCanvasContext = (canvasRef) => {
  if (!canvasRef) {
    console.warn('Canvas ref is null')
    return null
  }
  
  try {
    const ctx = canvasRef.getContext('2d')
    
    if (!ctx || !ctx.canvas) {
      console.warn('Invalid canvas context')
      return null
    }
    
    // Check canvas dimensions
    if (ctx.canvas.width === 0 || ctx.canvas.height === 0) {
      console.warn('Canvas has zero dimensions')
      return null
    }
    
    // Check if canvas is in DOM
    if (!document.contains(ctx.canvas)) {
      console.warn('Canvas is not attached to DOM')
      return null
    }
    
    return ctx
  } catch (error) {
    console.error('Failed to get canvas context:', error)
    return null
  }
}

/**
 * Destroy chart safely
 * @param {Object} chart - Chart.js instance
 */
export const destroyChart = (chart) => {
  if (chart && typeof chart.destroy === 'function') {
    try {
      chart.destroy()
    } catch (error) {
      console.warn('Error destroying chart:', error)
    }
  }
}

/**
 * Create common tooltip configuration
 * @param {Function} customFormatter - Custom formatter function
 * @returns {Object} Tooltip configuration
 */
export const createTooltipConfig = (customFormatter = null) => {
  return {
    enabled: true,
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    padding: 12,
    titleFont: { size: 14, weight: 'bold' },
    bodyFont: { size: 12 },
    cornerRadius: 8,
    callbacks: customFormatter || {}
  }
}

/**
 * Create common legend configuration
 * @param {string} position - Legend position
 * @returns {Object} Legend configuration
 */
export const createLegendConfig = (position = 'bottom') => {
  return {
    display: true,
    position,
    labels: {
      padding: 15,
      font: { size: 12 },
      usePointStyle: true
    }
  }
}

/**
 * Calculate statistics from array of values
 * @param {Array} values - Array of numeric values
 * @returns {Object} Statistics object
 */
export const calculateStatistics = (values) => {
  if (!values || values.length === 0) {
    return {
      min: 0,
      max: 0,
      mean: 0,
      median: 0,
      q1: 0,
      q3: 0
    }
  }
  
  const sorted = [...values].sort((a, b) => a - b)
  const n = sorted.length
  
  const getPercentile = (p) => {
    const index = (n - 1) * p
    const lower = Math.floor(index)
    const upper = Math.ceil(index)
    const weight = index - lower
    
    if (upper >= n) return sorted[n - 1]
    return sorted[lower] * (1 - weight) + sorted[upper] * weight
  }
  
  return {
    min: sorted[0],
    max: sorted[n - 1],
    mean: values.reduce((a, b) => a + b, 0) / n,
    median: getPercentile(0.5),
    q1: getPercentile(0.25),
    q3: getPercentile(0.75)
  }
}

/**
 * Filter valid clusters (exclude noise)
 * @param {Array} clusters - Array of cluster objects
 * @returns {Array} Filtered clusters
 */
export const filterValidClusters = (clusters) => {
  if (!clusters || !Array.isArray(clusters)) return []
  return clusters.filter(c => !isNoiseCluster(c))
}

/**
 * Get metric values from cluster members
 * @param {Object} cluster - Cluster object
 * @param {string} metric - Metric key
 * @returns {Array} Array of metric values
 */
export const getClusterMetricValues = (cluster, metric) => {
  if (!cluster.members || !Array.isArray(cluster.members)) return []
  
  return cluster.members
    .map(m => m[metric])
    .filter(v => v !== null && v !== undefined && !isNaN(v))
}

/**
 * Create debounced function
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
export const debounce = (func, wait = 300) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}
