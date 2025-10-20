# 📁 Project Structure

## Directory Organization

```
cluster-analysis-web/
├── backend/                      # Django Backend
│   ├── backend/                 # Django project settings
│   │   ├── settings.py         # Main configuration
│   │   ├── urls.py             # URL routing
│   │   └── wsgi.py             # WSGI application
│   │
│   ├── clustering/              # Main clustering app
│   │   ├── algorithms.py       # FCM & OPTICS algorithms
│   │   ├── cluster_interpreter.py  # Auto-labeling logic
│   │   ├── constants.py        # Backend constants
│   │   ├── models.py           # Database models
│   │   ├── pdf_generator.py   # PDF report generation
│   │   ├── utils.py            # Helper functions
│   │   └── views.py            # API endpoints
│   │
│   ├── tests/                   # Test files
│   │   ├── test_*.py           # Unit & integration tests
│   │   └── debug_*.py          # Debug scripts
│   │
│   ├── sample-data/             # Sample datasets
│   │   ├── *.xlsx              # Excel templates
│   │   ├── *.csv               # CSV samples
│   │   └── create_*.py         # Data generation scripts
│   │
│   ├── manage.py                # Django management
│   ├── requirements.txt         # Python dependencies
│   └── db.sqlite3               # SQLite database
│
├── fuzzy-clustering-frontend/   # Vue.js Frontend
│   ├── src/
│   │   ├── components/         # Vue components
│   │   │   ├── AllYearsResults.vue      # All years mode display
│   │   │   ├── YearlyResults.vue        # Per year mode display
│   │   │   ├── InteractiveMap.vue       # Geographic map
│   │   │   ├── ScatterPlot.vue          # Scatter visualization
│   │   │   ├── BoxPlot.vue              # Box plot visualization
│   │   │   ├── SilhouettePlot.vue       # Silhouette plot
│   │   │   ├── CorrelationHeatmap.vue   # Correlation matrix
│   │   │   └── ClusterDetailCard.vue    # Cluster info card
│   │   │
│   │   ├── views/              # Main pages
│   │   │   ├── Home.vue               # Landing page
│   │   │   ├── UploadEnhanced.vue     # Data upload page
│   │   │   └── AnalysisEnhanced.vue   # Results page
│   │   │
│   │   ├── services/           # API & services
│   │   │   ├── apiService.js         # API calls
│   │   │   └── pdfService.js         # PDF download
│   │   │
│   │   ├── utils/              # Utilities
│   │   │   ├── chartHelpers.js       # Chart utilities
│   │   │   └── constants.js          # Frontend constants
│   │   │
│   │   ├── data/               # Static data
│   │   │   └── cityCoordinates.js    # 495 Indonesian cities
│   │   │
│   │   ├── router/             # Vue Router
│   │   │   └── index.js
│   │   │
│   │   ├── assets/             # Static assets
│   │   │   └── css/
│   │   │       └── global.css
│   │   │
│   │   ├── App.vue             # Root component
│   │   └── main.js             # Application entry
│   │
│   ├── package.json            # NPM dependencies
│   └── vite.config.js          # Vite configuration
│
├── docs/                        # Documentation
│   ├── README.md               # Documentation index
│   ├── SETUP_GUIDE.md          # Installation guide
│   ├── API_DOCUMENTATION.md    # API reference
│   ├── FEATURES.md             # Feature list
│   └── *.md                    # Various documentation
│
├── setup.sh                     # Linux/Mac setup script
├── setup.bat                    # Windows setup script
└── README.md                    # Main project README
```

---

## Key Files Reference

### Backend Core Files

| File | Purpose | Lines |
|------|---------|-------|
| `algorithms.py` | Fuzzy C-Means & OPTICS implementation | ~400 |
| `cluster_interpreter.py` | Auto-label clusters based on characteristics | ~200 |
| `pdf_generator.py` | Generate comprehensive PDF reports | ~900 |
| `views.py` | API endpoints & request handling | ~500 |
| `utils.py` | Data validation & helper functions | ~300 |
| `constants.py` | Backend configuration constants | ~100 |

### Frontend Core Files

| File | Purpose | Components |
|------|---------|------------|
| `UploadEnhanced.vue` | File upload & parameter selection | Main page |
| `AnalysisEnhanced.vue` | Results display & visualization | Main page |
| `AllYearsResults.vue` | All years clustering results | Container |
| `YearlyResults.vue` | Per year clustering results | Container |
| `InteractiveMap.vue` | Geographic cluster distribution | Chart |
| `ScatterPlot.vue` | Feature scatter plots | Chart |
| `BoxPlot.vue` | Distribution box plots | Chart |
| `SilhouettePlot.vue` | Cluster quality visualization | Chart |
| `apiService.js` | API communication layer | Service |
| `chartHelpers.js` | Chart utility functions | Utility |
| `constants.js` | Frontend configuration | Config |

---

## File Naming Conventions

### Backend (Python)
- **Models:** `models.py` - Django models
- **Views:** `views.py` - API endpoints
- **Algorithms:** `algorithms.py` - Core algorithms
- **Utilities:** `utils.py`, `constants.py`
- **Services:** `{service_name}.py` (e.g., `pdf_generator.py`)
- **Tests:** `test_{module}.py`

### Frontend (Vue.js)
- **Components:** `PascalCase.vue` (e.g., `ScatterPlot.vue`)
- **Views/Pages:** `PascalCase.vue` with descriptive suffix (e.g., `UploadEnhanced.vue`)
- **Services:** `camelCase.js` (e.g., `apiService.js`)
- **Utilities:** `camelCase.js` (e.g., `chartHelpers.js`)
- **Data:** `camelCase.js` (e.g., `cityCoordinates.js`)

### Documentation
- **User docs:** `UPPERCASE_WITH_UNDERSCORES.md`
- **Feature docs:** Descriptive names (e.g., `PDF_EXPORT_FEATURE.md`)
- **Fix docs:** Issue-based (e.g., `BUGFIX_ALL_YEARS_UPLOAD.md`)

---

## Quick Navigation

### For Development
- **Start backend:** `cd backend && python manage.py runserver`
- **Start frontend:** `cd fuzzy-clustering-frontend && npm run dev`
- **Run tests:** `cd backend/tests && python test_*.py`

### For Documentation
- **See all docs:** `cd docs && ls *.md`
- **Feature list:** `docs/FEATURES.md`
- **Setup guide:** `docs/SETUP_GUIDE.md`
- **API docs:** `docs/API_DOCUMENTATION.md`

### For Deployment
- **Requirements:** `backend/requirements.txt`
- **Config:** `backend/backend/settings.py`
- **Static files:** `python manage.py collectstatic`

---

## Clean Code Practices Applied

✅ **Single Responsibility** - Each file has one clear purpose  
✅ **DRY Principle** - No code duplication  
✅ **Meaningful Names** - Self-documenting file/folder names  
✅ **Separation of Concerns** - Clear module boundaries  
✅ **Organized Structure** - Logical folder hierarchy  
✅ **Constants Extracted** - All magic values in constants files  
✅ **Utilities Centralized** - Shared functions in utils  
✅ **Tests Isolated** - All tests in dedicated folder  
✅ **Docs Organized** - All documentation in docs folder  
✅ **Samples Separated** - Sample data in dedicated folder  

---

## File Count Summary

| Category | Count | Location |
|----------|-------|----------|
| **Backend Python** | ~15 | `backend/clustering/` |
| **Frontend Components** | 8 | `src/components/` |
| **Frontend Views** | 3 | `src/views/` |
| **Services** | 2 | `src/services/` |
| **Utilities** | 2 | `src/utils/` |
| **Tests** | 10 | `backend/tests/` |
| **Sample Data** | 8 | `backend/sample-data/` |
| **Documentation** | 50+ | `docs/` |

---

**Total Lines of Code:** ~8,000 (backend) + ~5,000 (frontend) = **~13,000 lines**

**Well-organized, clean, and maintainable!** ✨
