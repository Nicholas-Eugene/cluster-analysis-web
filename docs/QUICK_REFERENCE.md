# 🚀 Quick Reference Guide - Clean Code

## 📌 Cheat Sheet untuk Developer

### Backend Quick Reference

#### 1. Import Constants
```python
from .constants import (
    # Column names
    COLUMN_IPM,
    COLUMN_GARIS_KEMISKINAN,
    COLUMN_PENGELUARAN_PER_KAPITA,
    
    # Algorithms
    ALGORITHM_FCM,
    ALGORITHM_OPTICS,
    
    # Modes
    MODE_PER_YEAR,
    MODE_ALL_YEARS,
    
    # Defaults
    DEFAULT_NUM_CLUSTERS,
    DEFAULT_FUZZY_COEFF,
)
```

#### 2. Import Utils
```python
from .utils import (
    # Data processing
    normalize_column_names,
    validate_required_columns,
    clean_and_validate_data,
    read_data_file,
    
    # Type conversion
    safe_float_conversion,
    safe_int_conversion,
    
    # Formatting
    format_clustering_parameters,
)
```

#### 3. Common Patterns

**Reading File:**
```python
# ✅ Clean way
from .utils import read_data_file

try:
    df = read_data_file(file_obj)
except ValueError as e:
    return Response({"error": str(e)}, status=400)
```

**Validating Data:**
```python
# ✅ Clean way
from .utils import normalize_column_names, validate_required_columns

df, mapping = normalize_column_names(df)
missing = validate_required_columns(df)

if missing:
    return Response({"error": f"Missing: {missing}"}, status=400)
```

**Safe Type Conversion:**
```python
# ✅ Clean way
from .utils import safe_int_conversion, safe_float_conversion

num_clusters = safe_int_conversion(request.POST.get("num_clusters"), DEFAULT_NUM_CLUSTERS)
fuzzy_coeff = safe_float_conversion(request.POST.get("fuzzy_coeff"), DEFAULT_FUZZY_COEFF)
```

---

### Frontend Quick Reference

#### 1. Import Constants
```javascript
import {
    // Colors
    CLUSTER_COLORS,
    
    // Labels
    METRIC_LABELS,
    METRIC_DISPLAY_NAMES,
    
    // Thresholds
    QUALITY_THRESHOLDS,
    
    // Chart defaults
    CHART_DEFAULTS,
    
    // API
    API_ENDPOINTS,
} from '@/utils/constants'
```

#### 2. Import Chart Helpers
```javascript
import {
    // Colors & labels
    getClusterColor,
    getClusterLabel,
    
    // Formatting
    formatCurrency,
    formatNumber,
    formatMetricLabel,
    
    // Canvas
    getValidCanvasContext,
    destroyChart,
    
    // Calculations
    calculateStatistics,
    
    // Utilities
    filterValidClusters,
    getClusterMetricValues,
    debounce,
} from '@/utils/chartHelpers'
```

#### 3. Common Patterns

**Getting Cluster Color:**
```javascript
// ✅ Clean way
import { getClusterColor } from '@/utils/chartHelpers'

const color = getClusterColor(clusterIndex)
```

**Formatting Values:**
```javascript
// ✅ Clean way
import { formatCurrency, formatNumber } from '@/utils/chartHelpers'

const formattedMoney = formatCurrency(value)
const formattedNum = formatNumber(value, 2) // 2 decimal places
```

**Validating Canvas:**
```javascript
// ✅ Clean way
import { getValidCanvasContext, destroyChart } from '@/utils/chartHelpers'

const ctx = getValidCanvasContext(chartCanvas.value)
if (!ctx) {
    console.warn('Invalid canvas')
    return
}

// Later...
destroyChart(chart.value)
```

**Calculating Statistics:**
```javascript
// ✅ Clean way
import { calculateStatistics } from '@/utils/chartHelpers'

const values = cluster.members.map(m => m.ipm)
const stats = calculateStatistics(values)
// Returns: { min, max, mean, median, q1, q3 }
```

---

## 🎯 Common Tasks

### Task 1: Menambahkan Metric Baru

**Backend (constants.py):**
```python
# Add column name
COLUMN_NEW_METRIC = "new_metric"

# Add to required columns
REQUIRED_COLUMNS = {
    ...existing...,
    COLUMN_NEW_METRIC: ["new_metric", "newmetric"],
}

# Add to clustering features
CLUSTERING_FEATURES = [
    COLUMN_IPM,
    COLUMN_GARIS_KEMISKINAN,
    COLUMN_PENGELUARAN_PER_KAPITA,
    COLUMN_NEW_METRIC,  # Add this
]
```

**Frontend (constants.js):**
```javascript
// Add label
export const METRIC_LABELS = {
    ...existing...,
    new_metric: 'New Metric Label',
}
```

### Task 2: Mengubah Default Parameters

**Edit `backend/clustering/constants.py`:**
```python
# Change defaults here
DEFAULT_NUM_CLUSTERS = 3  # Change to 4, 5, etc.
DEFAULT_FUZZY_COEFF = 2.0  # Change to 1.5, 2.5, etc.
```

**Edit `frontend/src/utils/constants.js`:**
```javascript
export const DEFAULT_FORM_VALUES = {
    algorithm: ALGORITHMS.FCM,
    numClusters: 3,  // Change here
    fuzzyCoeff: 2.0,  // Change here
    ...
}
```

### Task 3: Menambahkan Cluster Color Baru

**Edit `frontend/src/utils/constants.js`:**
```javascript
export const CLUSTER_COLORS = [
    '#667eea',
    '#48bb78',
    '#ed8936',
    '#4299e1',
    '#f56565',
    '#38b2ac',
    '#9f7aea',
    '#ecc94b',
    '#f687b3',
    '#4fd1c5',
    '#your-new-color',  // Add here
]
```

### Task 4: Mengubah Quality Thresholds

**Backend (constants.py):**
```python
# Interpretation thresholds
THRESHOLD_LOW = 0.33   # Change here
THRESHOLD_HIGH = 0.67  # Change here
```

**Frontend (constants.js):**
```javascript
export const QUALITY_THRESHOLDS = {
    davies_bouldin: {
        excellent: 1.0,   // Change here
        good: 1.5,        // Change here
        fair: 2.0         // Change here
    },
    silhouette: {
        excellent: 0.7,   // Change here
        good: 0.5,        // Change here
        fair: 0.25        // Change here
    }
}
```

---

## 🔧 Troubleshooting

### Import Error di Backend

**Problem:**
```python
ImportError: cannot import name 'ALGORITHM_FCM'
```

**Solution:**
```python
# Check if you imported from correct module
from .constants import ALGORITHM_FCM  # ✅ Correct
from constants import ALGORITHM_FCM   # ❌ Wrong (missing dot)
```

### Import Error di Frontend

**Problem:**
```javascript
Module not found: Can't resolve '@/utils/constants'
```

**Solution:**
```javascript
// Make sure file exists and path is correct
import { CLUSTER_COLORS } from '@/utils/constants'  // ✅ Correct

// Check vite.config.js for @ alias:
// alias: {
//   '@': path.resolve(__dirname, './src'),
// }
```

### Function Not Found

**Problem:**
```python
NameError: name 'safe_float_conversion' is not defined
```

**Solution:**
```python
# Import the function
from .utils import safe_float_conversion  # Add this import
```

---

## 📝 Code Style Guidelines

### Python (Backend)

```python
# ✅ Good
def calculate_average_metrics(
    results_per_year: Dict, 
    metric_name: str
) -> Optional[float]:
    """
    Calculate average of a metric across all years.
    
    Args:
        results_per_year: Dictionary of results per year
        metric_name: Name of the metric to average
        
    Returns:
        Average value or None if no valid values
    """
    # Implementation...
    pass

# ✅ Use constants
if algorithm == ALGORITHM_FCM:
    pass

# ✅ Use utils
value = safe_float_conversion(data.get("value"), 0.0)

# ✅ Clear variable names
total_clusters = len(clusters)
average_silhouette_score = calculate_average(scores)
```

### JavaScript (Frontend)

```javascript
// ✅ Good
/**
 * Calculate statistics from array of values
 * @param {Array} values - Array of numeric values
 * @returns {Object} Statistics object
 */
export const calculateStatistics = (values) => {
    // Implementation...
}

// ✅ Use constants
import { CLUSTER_COLORS } from '@/utils/constants'

// ✅ Use helpers
import { getClusterColor, formatCurrency } from '@/utils/chartHelpers'

// ✅ Clear variable names
const clusterColor = getClusterColor(index)
const formattedPrice = formatCurrency(price)
```

---

## 🎨 Naming Conventions

### Backend

- **Constants:** `UPPER_SNAKE_CASE`
  ```python
  ALGORITHM_FCM = "fcm"
  DEFAULT_NUM_CLUSTERS = 3
  ```

- **Functions:** `snake_case`
  ```python
  def read_data_file(file_obj):
      pass
  ```

- **Classes:** `PascalCase`
  ```python
  class ClusteringAlgorithms:
      pass
  ```

- **Variables:** `snake_case`
  ```python
  num_clusters = 3
  fuzzy_coeff = 2.0
  ```

### Frontend

- **Constants:** `UPPER_SNAKE_CASE`
  ```javascript
  export const CLUSTER_COLORS = [...]
  ```

- **Functions:** `camelCase`
  ```javascript
  export const getClusterColor = (index) => {...}
  ```

- **Components:** `PascalCase`
  ```javascript
  export default {
      name: 'ScatterPlot',
  }
  ```

- **Variables:** `camelCase`
  ```javascript
  const clusterColor = getClusterColor(index)
  ```

---

## 📚 File Organization

### Ketika Membuat File Baru

**Backend:**
```
backend/clustering/
├── constants.py       # Add constants here
├── utils.py           # Add utility functions here
├── algorithms.py      # Add algorithm logic here
├── views.py          # Add API endpoints here
└── your_new_file.py  # New feature modules
```

**Frontend:**
```
frontend/src/
├── utils/
│   ├── constants.js      # Add constants here
│   ├── chartHelpers.js   # Add chart helpers here
│   └── yourHelpers.js    # New utility modules
├── components/           # Add components here
└── services/            # Add API services here
```

---

## ✅ Checklist untuk Pull Request

Sebelum submit code:

- [ ] Menggunakan constants (tidak ada magic numbers/strings)
- [ ] Menggunakan utility functions yang ada (tidak duplikasi)
- [ ] Nama variabel/fungsi deskriptif
- [ ] Fungsi kecil (< 30-40 lines)
- [ ] Ada docstring/comments untuk fungsi public
- [ ] No linter errors
- [ ] Code formatted dengan benar
- [ ] Import statements terorganisir

---

**Happy Coding! 🎉**
