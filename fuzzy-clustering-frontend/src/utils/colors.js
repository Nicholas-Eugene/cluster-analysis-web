// Design System - Color Palette
// Centralized color management for consistent UI across all components

// Primary Color Palette - Purple Gradient Theme
export const PRIMARY_COLORS = {
  purple: {
    50: '#faf5ff',
    100: '#f3e8ff',
    200: '#e9d5ff',
    300: '#d8b4fe',
    400: '#c084fc',
    500: '#a855f7',
    600: '#9333ea',
    700: '#7e22ce',
    800: '#6b21a8',
    900: '#581c87',
  },
  gradient: {
    primary: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    light: 'linear-gradient(135deg, #e6f7ff 0%, #f0f9ff 100%)',
    success: 'linear-gradient(135deg, #48bb78 0%, #38a169 100%)',
    warning: 'linear-gradient(135deg, #ed8936 0%, #dd6b20 100%)',
    info: 'linear-gradient(135deg, #4299e1 0%, #3182ce 100%)',
    danger: 'linear-gradient(135deg, #f56565 0%, #e53e3e 100%)',
  }
}

// Cluster Colors - Used for all visualizations
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

// Cluster Colors with Alpha (for transparency)
export const getClusterColorWithAlpha = (index, alpha = 1) => {
  const color = CLUSTER_COLORS[index % CLUSTER_COLORS.length]
  return hexToRgba(color, alpha)
}

// Helper function to convert hex to rgba
function hexToRgba(hex, alpha) {
  const r = parseInt(hex.slice(1, 3), 16)
  const g = parseInt(hex.slice(3, 5), 16)
  const b = parseInt(hex.slice(5, 7), 16)
  return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

// Heatmap Colors - For correlation visualization
export const HEATMAP_COLORS = {
  positive: {
    light: '#fef3c7',
    base: '#667eea',
    dark: '#4c51bf',
  },
  negative: {
    light: '#dbeafe',
    base: '#48bb78',
    dark: '#2f855a',
  },
  neutral: '#ffffff',
}

// Get correlation color based on value (-1 to 1)
export const getCorrelationColor = (correlation) => {
  const absCorr = Math.abs(correlation)
  
  if (correlation > 0) {
    // Positive correlation: white to purple
    return hexToRgba(HEATMAP_COLORS.positive.base, absCorr * 0.9)
  } else if (correlation < 0) {
    // Negative correlation: white to green
    return hexToRgba(HEATMAP_COLORS.negative.base, absCorr * 0.9)
  } else {
    // No correlation: white
    return HEATMAP_COLORS.neutral
  }
}

// Get correlation color for gradient legend
export const getCorrelationGradient = () => {
  return `linear-gradient(90deg, 
    ${HEATMAP_COLORS.negative.base} 0%, 
    ${HEATMAP_COLORS.neutral} 50%, 
    ${HEATMAP_COLORS.positive.base} 100%
  )`
}

// UI Element Colors
export const UI_COLORS = {
  background: {
    primary: '#ffffff',
    secondary: '#f7fafc',
    tertiary: '#edf2f7',
    card: '#ffffff',
    hover: '#f7fafc',
  },
  text: {
    primary: '#2d3748',
    secondary: '#4a5568',
    tertiary: '#718096',
    light: '#a0aec0',
    white: '#ffffff',
  },
  border: {
    light: '#e2e8f0',
    medium: '#cbd5e0',
    dark: '#a0aec0',
  },
  status: {
    success: '#48bb78',
    warning: '#ed8936',
    error: '#f56565',
    info: '#4299e1',
  },
  quality: {
    excellent: '#38a169',
    good: '#48bb78',
    fair: '#ed8936',
    poor: '#f56565',
    unknown: '#718096',
  }
}

// Shadow Tokens
export const SHADOWS = {
  sm: '0 1px 3px rgba(0, 0, 0, 0.1)',
  md: '0 4px 6px rgba(0, 0, 0, 0.1)',
  lg: '0 10px 15px rgba(0, 0, 0, 0.1)',
  xl: '0 20px 25px rgba(0, 0, 0, 0.15)',
  purple: '0 4px 12px rgba(102, 126, 234, 0.15)',
  hover: '0 4px 12px rgba(102, 126, 234, 0.2)',
}

// Border Radius Tokens
export const BORDER_RADIUS = {
  sm: '4px',
  md: '8px',
  lg: '12px',
  xl: '16px',
  full: '9999px',
}

// Spacing Tokens
export const SPACING = {
  xs: '0.25rem',
  sm: '0.5rem',
  md: '1rem',
  lg: '1.5rem',
  xl: '2rem',
  '2xl': '3rem',
  '3xl': '4rem',
}

// Export default color getter for backward compatibility
export const getClusterColor = (index) => {
  return CLUSTER_COLORS[index % CLUSTER_COLORS.length]
}

export default {
  PRIMARY_COLORS,
  CLUSTER_COLORS,
  HEATMAP_COLORS,
  UI_COLORS,
  SHADOWS,
  BORDER_RADIUS,
  SPACING,
  getClusterColor,
  getClusterColorWithAlpha,
  getCorrelationColor,
  getCorrelationGradient,
}
