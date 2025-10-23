# 🌏 Fuzzy Clustering Analysis - Indonesian Regions

<div align="center">

**Analisis Clustering Wilayah Indonesia menggunakan Fuzzy C-Means & OPTICS**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-green.svg)](https://vuejs.org)
[![Django](https://img.shields.io/badge/Django-5.2+-darkgreen.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Documentation](#-documentation) • [Screenshots](#-screenshots)

</div>

---

## 📖 Overview

Aplikasi web untuk analisis clustering wilayah Indonesia berdasarkan indikator pembangunan:
- **IPM** (Indeks Pembangunan Manusia)
- **Garis Kemiskinan**  
- **Pengeluaran Per Kapita**

Menggunakan algoritma **Fuzzy C-Means** dan **OPTICS** untuk mengelompokkan 514 kabupaten/kota di Indonesia menjadi cluster dengan karakteristik serupa.

---

## ✨ Features

### 🎯 Core Features

- **📊 Dual Algorithm Support**
  - Fuzzy C-Means (FCM) - Soft clustering
  - OPTICS - Density-based clustering with noise detection

- **📈 Dual Analysis Mode**
  - **All Years Mode** - Aggregate analysis across all years
  - **Per Year Mode** - Year-by-year trend analysis

- **🤖 Auto-Interpretation**
  - Automatically labels clusters (e.g., "Daerah Maju Biaya Tinggi")
  - Generates descriptions based on characteristics
  - 8 category classifications

- **🗺️ Geographic Visualization**
  - Interactive map with 495 Indonesian cities
  - Auto-mapped coordinates for all regions
  - Color-coded cluster distribution

### 📊 Visualizations

- **Scatter Plots** - Feature correlation analysis
- **Box Plots** - Distribution comparison across clusters
- **Silhouette Plots** - Cluster quality assessment
- **Correlation Heatmaps** - Feature relationship matrix
- **Geographic Maps** - Spatial distribution visualization

### 📄 PDF Export

- **Comprehensive Reports** - All visualizations included
- **Cluster Details** - Interpretation labels, members list
- **Quality Metrics** - Davies-Bouldin, Silhouette scores
- **Memory Efficient** - Works on 500MB RAM (no Playwright)

### 💅 UI/UX

- **Modern Design** - Purple gradient theme
- **Responsive Layout** - Works on mobile, tablet, desktop
- **Real-time Updates** - Live clustering status
- **Interactive Charts** - Zoom, pan, tooltips
- **Error Handling** - Clear error messages

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**

### Installation

#### Option 1: Automated Setup

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bash
setup.bat
```

#### Option 2: Manual Setup

**1. Clone Repository**
```bash
git clone <repository-url>
cd cluster-analysis-web
```

**2. Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**3. Frontend Setup** (new terminal)
```bash
cd fuzzy-clustering-frontend
npm install
npm run dev
```

**4. Open Browser**
```
http://localhost:5173
```

---

## 📚 Documentation

### Essential Docs

- **[Setup Guide](docs/SETUP_GUIDE.md)** - Detailed installation
- **[Features](docs/COMPLETE_SUMMARY_ALL_FEATURES.md)** - Complete feature list
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Directory organization
- **[API Documentation](docs/API_DOCUMENTATION.md)** - API reference

### Development Docs

- **[Clean Code Guide](docs/CLEAN_CODE_GUIDE.md)** - Best practices
- **[Code Cleanup](docs/CODE_CLEANUP_COMPLETE.md)** - Organization changes
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Common commands

### Feature Docs

- **[Cluster Interpretation](docs/CLUSTER_INTERPRETATION_FEATURE.md)**
- **[PDF Export](docs/PDF_EXPORT_FEATURE.md)**
- **[Geographic Mapping](docs/FOLIUM_MAP_IMPLEMENTATION.md)**
- **[Per-Year Analysis](docs/CLUSTERING_PER_TAHUN.md)**

**See [docs/README.md](docs/README.md) for complete index** (50+ documents)

---

## 🖼️ Screenshots

### Upload Page
Modern interface untuk upload data dan konfigurasi parameter

### Analysis Results
Comprehensive visualizations dengan interpretasi otomatis

### Interactive Map
Geographic distribution 495 kota di Indonesia

### PDF Report
Professional quality report dengan semua visualizations

*(Screenshots akan ditambahkan)*

---

## 🏗️ Tech Stack

### Backend
- **Django 5.2** - Web framework
- **Django REST Framework** - API endpoints
- **scikit-learn** - Machine learning algorithms
- **scikit-fuzzy** - Fuzzy C-Means implementation
- **pandas** - Data processing
- **matplotlib** - Visualizations
- **ReportLab** - PDF generation

### Frontend
- **Vue.js 3** - Progressive framework
- **Vue Router** - Page routing
- **Chart.js** - Interactive charts
- **Axios** - HTTP client
- **Vite** - Build tool

---

## 📊 Algorithms

### Fuzzy C-Means (FCM)

**Soft clustering** - Each data point has membership degree to all clusters

**Parameters:**
- Number of clusters (2-10)
- Fuzzy coefficient (1.0-3.0, default: 2.0)
- Maximum iterations (default: 150)
- Error tolerance (default: 0.0001)

**Use Case:** When boundaries between groups are fuzzy

### OPTICS

**Density-based** - Automatically finds clusters and detects noise/outliers

**Parameters:**
- Minimum samples (default: 5)
- Maximum epsilon (default: auto)
- Minimum cluster size (default: 10)

**Use Case:** When you don't know number of clusters beforehand

---

## 📈 Auto-Interpretation System

Automatically labels clusters into 8 categories:

| Category | IPM | Garis Kemiskinan | Pengeluaran |
|----------|-----|------------------|-------------|
| 🏆 **Daerah Maju Biaya Tinggi** | Tinggi | Tinggi | Tinggi |
| 💰 **Daerah Maju Biaya Rendah** | Tinggi | Rendah | Tinggi |
| 📈 **Daerah Berkembang Potensial** | Sedang | Sedang | Tinggi |
| 🎯 **Daerah Berkembang Stabil** | Sedang | Sedang | Sedang |
| ⚠️ **Daerah Berkembang Tertantang** | Sedang | Tinggi | Rendah |
| 📉 **Daerah Tertinggal Berat** | Rendah | Rendah | Rendah |
| 🆘 **Daerah Tertinggal Sangat Berat** | Rendah | Tinggi | Rendah |
| ❓ **Daerah Karakteristik Campuran** | Mixed | Mixed | Mixed |

---

## 🗺️ Geographic Coverage

**495 Indonesian Cities/Regencies** mapped with coordinates

Coverage includes:
- ✅ All 38 provinces
- ✅ All major cities
- ✅ Most regencies (kabupaten)
- ✅ Jakarta administrative regions
- ✅ Special autonomous regions

**Coordinate Source:** `fuzzy-clustering-frontend/src/data/cityCoordinates.js`

---

## 🎯 Use Cases

### Research
- Analisis kesenjangan pembangunan regional
- Identifikasi pola geografis kemiskinan
- Evaluasi efektivitas kebijakan

### Government
- Prioritasi alokasi anggaran
- Perencanaan pembangunan daerah
- Monitoring progress SDGs

### Education
- Pembelajaran machine learning
- Studi kasus clustering algorithms
- Visualisasi data geospasial

---

## 💻 Development

### Project Structure

```
cluster-analysis-web/
├── backend/              # Django backend
│   ├── clustering/      # Main app (algorithms, PDF, API)
│   ├── tests/           # Test files
│   └── sample-data/     # Sample datasets
├── frontend/            # Vue.js frontend
│   └── src/
│       ├── components/  # Vue components
│       ├── views/       # Main pages
│       ├── services/    # API services
│       └── utils/       # Utilities
└── docs/                # Documentation (50+ files)
```

See [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) for detailed structure.

### Code Quality

✅ **Clean Code** - Following best practices  
✅ **Well Documented** - 50+ documentation files  
✅ **Tested** - Unit & integration tests  
✅ **Organized** - Clear folder structure  
✅ **Maintainable** - ~13,000 lines, clean architecture  

---

## 🚀 Deployment

### Low Memory (500MB RAM)

Application optimized for deployment on:
- Heroku (Free/Eco tier)
- Railway
- Render
- Fly.io
- DigitalOcean App Platform

**Memory Usage:** ~150-250 MB at peak

See [docs/LOW_MEMORY_DEPLOYMENT.md](docs/LOW_MEMORY_DEPLOYMENT.md)

### Production Checklist

- [ ] Set `DEBUG=False` in settings.py
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set `SECRET_KEY` environment variable
- [ ] Run `python manage.py collectstatic`
- [ ] Run `python manage.py migrate`
- [ ] Setup process manager (Gunicorn)
- [ ] Configure reverse proxy (Nginx)

---

## 🧪 Testing

### Run Tests

```bash
# Backend tests
cd backend/tests
python test_endpoints.py
python test_optics.py

# All tests
cd backend/tests
python -m pytest
```

### Test Coverage

- ✅ API endpoints
- ✅ Clustering algorithms
- ✅ Data processing
- ✅ PDF generation
- ✅ Cluster interpretation

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests
5. Update documentation
6. Submit pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 👥 Authors

**Development Team**
- Backend Development
- Frontend Development  
- Algorithm Implementation
- Documentation

---

## 🙏 Acknowledgments

- **Data Source:** BPS (Badan Pusat Statistik)
- **Algorithms:** scikit-learn, scikit-fuzzy
- **Frameworks:** Django, Vue.js
- **Libraries:** Chart.js, ReportLab, matplotlib

---

## 📞 Support

### Documentation
- **Full Docs:** [docs/README.md](docs/README.md)
- **FAQ:** [docs/FAQ.md](docs/FAQ.md)
- **Troubleshooting:** [docs/QUICK_DEBUG_GUIDE.md](docs/QUICK_DEBUG_GUIDE.md)

### Issues
Found a bug? [Create an issue](../../issues)

### Questions
Have questions? [Start a discussion](../../discussions)

---

## 🗺️ Roadmap

### Completed ✅
- [x] Fuzzy C-Means algorithm
- [x] OPTICS algorithm
- [x] Auto-interpretation system
- [x] Geographic visualization
- [x] PDF export
- [x] Per-year analysis
- [x] Low memory optimization

### Planned 🚧
- [ ] User authentication
- [ ] Save analysis sessions
- [ ] Export to Excel
- [ ] Advanced filtering
- [ ] Comparison between years
- [ ] API documentation (Swagger)
- [ ] Docker deployment

---

## 📊 Statistics

- **Lines of Code:** ~13,000
- **Backend Files:** 15 core files
- **Frontend Components:** 8 components
- **Documentation Pages:** 50+
- **Supported Cities:** 495
- **Supported Provinces:** 38
- **Algorithms:** 2 (FCM, OPTICS)
- **Chart Types:** 5
- **Export Formats:** PDF

---

<div align="center">

**Made with ❤️ for Indonesian Development Analysis**

[⬆ Back to Top](#-fuzzy-clustering-analysis---indonesian-regions)

</div>
