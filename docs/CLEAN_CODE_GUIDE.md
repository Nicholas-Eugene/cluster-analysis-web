# 🧹 Clean Code Guide - Fuzzy Clustering Application

## 📋 Daftar Isi
- [Pengenalan](#pengenalan)
- [Struktur Proyek](#struktur-proyek)
- [Prinsip Clean Code yang Diterapkan](#prinsip-clean-code-yang-diterapkan)
- [Backend Architecture](#backend-architecture)
- [Frontend Architecture](#frontend-architecture)
- [Cara Memahami Kode](#cara-memahami-kode)

---

## 🎯 Pengenalan

Aplikasi ini telah di-refactor mengikuti prinsip **Clean Code** untuk meningkatkan:
- ✅ **Readability** - Kode mudah dibaca dan dipahami
- ✅ **Maintainability** - Mudah di-maintain dan dikembangkan
- ✅ **Reusability** - Mengurangi duplikasi kode
- ✅ **Testability** - Mudah untuk di-test
- ✅ **Documentation** - Dokumentasi yang jelas dan lengkap

---

## 📁 Struktur Proyek

### Backend Structure
```
backend/clustering/
├── constants.py              # ⚙️ Semua konstanta aplikasi
├── utils.py                  # 🛠️ Fungsi utility yang reusable
├── algorithms.py             # 🧮 Core algoritma clustering
├── cluster_interpreter.py    # 🏷️ Interpretasi otomatis cluster
├── views.py                  # 🌐 API endpoints (sudah di-refactor)
├── pdf_generator.py          # 📄 Generator laporan PDF
├── models.py                 # 💾 Database models
└── urls.py                   # 🔗 URL routing
```

### Frontend Structure
```
frontend/src/
├── utils/
│   ├── constants.js          # ⚙️ Konstanta frontend
│   ├── chartHelpers.js       # 📊 Helper functions untuk charts
│   └── colors.js             # 🎨 Color utilities
├── components/               # 🧩 Vue components
├── services/                 # 🔌 API service layer
└── router/                   # 🛣️ Routing configuration
```

---

## 🎨 Prinsip Clean Code yang Diterapkan

### 1. **Single Responsibility Principle (SRP)**
Setiap fungsi/class hanya memiliki satu tanggung jawab.

#### ❌ Sebelum (Bad):
```python
def process_file(file_obj):
    # Reading file
    df = pd.read_csv(file_obj)
    # Validating columns
    if 'ipm' not in df.columns:
        raise ValueError("Missing column")
    # Cleaning data
    df = df.dropna()
    # Running clustering
    results = run_clustering(df)
    return results
```

#### ✅ Sesudah (Good):
```python
def process_file(file_obj):
    df = read_data_file(file_obj)           # 1 tanggung jawab
    validate_required_columns(df)            # 1 tanggung jawab
    df_clean = clean_and_validate_data(df)  # 1 tanggung jawab
    return df_clean

def read_data_file(file_obj):
    """Read data from CSV or Excel file."""
    # Implementation...
```

### 2. **DRY (Don't Repeat Yourself)**
Hindari duplikasi kode dengan membuat fungsi yang reusable.

#### File: `backend/clustering/utils.py`
```python
def safe_float_conversion(value, default: float = 0.0) -> float:
    """Safely convert value to float with default fallback."""
    try:
        return float(value) if value is not None else default
    except (ValueError, TypeError):
        return default
```

Digunakan di banyak tempat tanpa duplikasi:
```python
fuzzy_coeff = safe_float_conversion(request.POST.get("fuzzy_coeff"), 2.0)
tolerance = safe_float_conversion(request.POST.get("tolerance"), 0.0001)
```

### 3. **Meaningful Names**
Gunakan nama yang deskriptif dan self-explanatory.

#### ❌ Bad:
```python
def proc(d, a, n):
    r = []
    for i in range(n):
        x = run_alg(d, a)
        r.append(x)
    return r
```

#### ✅ Good:
```python
def run_clustering_per_year(dataframe, algorithm, num_clusters):
    """
    Run clustering analysis for each year in the dataset.
    
    Args:
        dataframe: Input data with year column
        algorithm: Clustering algorithm to use (fcm or optics)
        num_clusters: Number of clusters to create
    
    Returns:
        Dictionary containing results for each year
    """
    results = []
    for year in dataframe['tahun'].unique():
        year_results = execute_clustering(dataframe, algorithm, year)
        results.append(year_results)
    return results
```

### 4. **Constants Instead of Magic Numbers**

#### ❌ Bad:
```python
if score < 0.33:
    quality = "poor"
elif score < 0.67:
    quality = "fair"
```

#### ✅ Good:
```python
# In constants.py
THRESHOLD_LOW = 0.33
THRESHOLD_HIGH = 0.67

# In code
if score < THRESHOLD_LOW:
    quality = "poor"
elif score < THRESHOLD_HIGH:
    quality = "fair"
```

### 5. **Separation of Concerns**

Backend dibagi menjadi layer yang jelas:
- **Constants Layer** (`constants.py`) - Konfigurasi
- **Utility Layer** (`utils.py`) - Helper functions
- **Business Logic Layer** (`algorithms.py`) - Core logic
- **API Layer** (`views.py`) - HTTP handling
- **Data Layer** (`models.py`) - Database

---

## 🔧 Backend Architecture

### Constants (`constants.py`)
Semua nilai konstan disimpan di satu tempat:

```python
# Column names
COLUMN_IPM = "ipm"
COLUMN_GARIS_KEMISKINAN = "garis_kemiskinan"

# Algorithm names
ALGORITHM_FCM = "fcm"
ALGORITHM_OPTICS = "optics"

# Default parameters
DEFAULT_NUM_CLUSTERS = 3
DEFAULT_FUZZY_COEFF = 2.0
```

**Keuntungan:**
- ✅ Mudah untuk mengubah nilai
- ✅ Konsisten di seluruh aplikasi
- ✅ Self-documenting

### Utils (`utils.py`)
Fungsi-fungsi utility yang reusable:

```python
# Data validation
normalize_column_names(df)
validate_required_columns(df)
clean_and_validate_data(df)

# File handling
read_data_file(file_obj)

# Type conversion
safe_float_conversion(value, default)
safe_int_conversion(value, default)

# Calculations
calculate_average_metrics(results, metric_name)
```

### Views (views.py) - Refactored
Sekarang lebih terstruktur dengan helper methods:

```python
class UploadAndProcessView(APIView):
    def post(self, request):
        # Main handler - orchestrates the process
        ...
    
    def _parse_selected_years(self, json_string):
        # Helper: Parse year selection
        ...
    
    def _execute_clustering(self, **params):
        # Helper: Execute clustering logic
        ...
    
    def _run_all_years_clustering(self, **params):
        # Helper: All years mode
        ...
    
    def _run_per_year_clustering(self, **params):
        # Helper: Per year mode
        ...
```

---

## 🎨 Frontend Architecture

### Constants (`utils/constants.js`)

```javascript
// Cluster colors - consistent across app
export const CLUSTER_COLORS = [
  '#667eea', '#48bb78', '#ed8936', ...
]

// Metric labels
export const METRIC_LABELS = {
  ipm: 'IPM',
  garis_kemiskinan: 'Garis Kemiskinan (Rp)',
  ...
}

// Quality thresholds
export const QUALITY_THRESHOLDS = {
  davies_bouldin: { excellent: 1.0, good: 1.5, ... }
}
```

### Chart Helpers (`utils/chartHelpers.js`)

Fungsi-fungsi reusable untuk charts:

```javascript
// Color management
getClusterColor(index)

// Label formatting
getClusterLabel(cluster)
formatMetricLabel(metric)
formatCurrency(value)
formatNumber(value, decimals)

// Validations
getValidCanvasContext(canvasRef)
isNoiseCluster(cluster)

// Utilities
calculateStatistics(values)
filterValidClusters(clusters)
getClusterMetricValues(cluster, metric)
destroyChart(chart)
debounce(func, wait)
```

**Penggunaan di Component:**

#### ❌ Sebelum (Duplikasi di setiap component):
```javascript
// ScatterPlot.vue
const colors = ['#667eea', '#48bb78', ...]
const getColor = (i) => colors[i % colors.length]

// BoxPlot.vue  
const colors = ['#667eea', '#48bb78', ...]  // ❌ DUPLIKASI!
const getColor = (i) => colors[i % colors.length]

// SilhouettePlot.vue
const colors = ['#667eea', '#48bb78', ...]  // ❌ DUPLIKASI!
const getColor = (i) => colors[i % colors.length]
```

#### ✅ Sesudah (Reusable):
```javascript
// Di semua components
import { getClusterColor, getClusterLabel } from '@/utils/chartHelpers'

// Langsung pakai
const color = getClusterColor(index)
const label = getClusterLabel(cluster)
```

---

## 📖 Cara Memahami Kode

### 1. **Mulai dari Constants**
Lihat `constants.py` atau `constants.js` untuk memahami konfigurasi aplikasi.

### 2. **Pahami Utils**
Baca `utils.py` atau `chartHelpers.js` untuk melihat fungsi-fungsi helper yang tersedia.

### 3. **Trace Flow**
Untuk memahami alur aplikasi:

#### Backend Flow:
```
1. views.py (API endpoint)
   ↓
2. utils.py (validation & preprocessing)
   ↓
3. algorithms.py (clustering logic)
   ↓
4. cluster_interpreter.py (interpretasi)
   ↓
5. Return results
```

#### Frontend Flow:
```
1. Component receives data
   ↓
2. Use chartHelpers for processing
   ↓
3. Apply constants for styling
   ↓
4. Render visualization
```

### 4. **Baca Dokumentasi Fungsi**
Setiap fungsi memiliki docstring yang menjelaskan:
- Apa yang dilakukan fungsi
- Parameter yang diterima
- Nilai yang dikembalikan
- Contoh penggunaan (jika perlu)

```python
def normalize_column_names(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """
    Normalize column names to standard format and create mapping.
    
    Args:
        df: Input dataframe with potentially varying column names
        
    Returns:
        Tuple of (normalized dataframe, column mapping dictionary)
    """
```

---

## 🎯 Best Practices untuk Development

### 1. **Selalu gunakan Constants**
```python
# ❌ Bad
if algorithm == "fcm":
    ...

# ✅ Good
from .constants import ALGORITHM_FCM
if algorithm == ALGORITHM_FCM:
    ...
```

### 2. **Gunakan Utility Functions**
Jangan buat ulang fungsi yang sudah ada di utils.

```python
# ❌ Bad
try:
    value = float(request.POST.get("num"))
except:
    value = 3

# ✅ Good
from .utils import safe_float_conversion
value = safe_float_conversion(request.POST.get("num"), 3)
```

### 3. **Import dengan Jelas**
```python
# ✅ Good - Explicit imports
from .constants import (
    ALGORITHM_FCM,
    ALGORITHM_OPTICS,
    DEFAULT_NUM_CLUSTERS
)
```

### 4. **Pisahkan Logic dari Presentation**
- Backend: Logic terpisah dari API handling
- Frontend: Business logic terpisah dari UI components

### 5. **Write Self-Documenting Code**
- Gunakan nama yang deskriptif
- Tambahkan comments hanya untuk logic yang kompleks
- Write docstrings untuk semua public functions

---

## 🔍 Contoh Refactoring

### Before vs After

#### ❌ **Before**: Monolithic function
```python
def upload_and_process(request):
    file = request.FILES.get("file")
    df = pd.read_csv(file)
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    if 'ipm' not in df.columns or 'tahun' not in df.columns:
        return {"error": "Missing columns"}
    df = df.dropna()
    df['ipm'] = pd.to_numeric(df['ipm'])
    algorithm = request.POST.get("algorithm", "fcm")
    num_clusters = int(request.POST.get("num_clusters", 3))
    # ... 50 more lines of mixed logic
```

#### ✅ **After**: Clean, modular functions
```python
def upload_and_process(request):
    """Process uploaded file and run clustering."""
    # Read file
    file = request.FILES.get("file")
    df = read_data_file(file)
    
    # Validate and clean
    df, mapping = normalize_column_names(df)
    missing = validate_required_columns(df)
    if missing:
        return {"error": f"Missing columns: {missing}"}
    
    df = clean_and_validate_data(df)
    
    # Parse parameters
    params = parse_clustering_parameters(request.POST)
    
    # Execute clustering
    results = execute_clustering(df, params)
    
    return results
```

---

## 📚 Kesimpulan

Dengan menerapkan clean code:

✅ **Kode lebih mudah dipahami** - Developer baru bisa cepat onboarding  
✅ **Maintenance lebih mudah** - Bug mudah dilacak dan diperbaiki  
✅ **Development lebih cepat** - Reuse existing utilities  
✅ **Fewer bugs** - Clear responsibilities dan validations  
✅ **Better collaboration** - Consistent coding style  

---

## 🤝 Contributing

Saat menambahkan fitur baru:

1. **Check constants** - Apakah perlu konstanta baru?
2. **Check utils** - Apakah ada utility yang bisa direuse?
3. **Follow naming conventions** - Gunakan nama yang deskriptif
4. **Add documentation** - Tambahkan docstrings
5. **Keep functions small** - Max 30-40 lines per function
6. **Write clean code** - Follow existing patterns

---

**Happy Coding! 🚀**
