# Indonesian Regional Clustering Web Application

A comprehensive web application for clustering Indonesian kabupaten/kota based on Human Development Index (IPM), Poverty Line (Garis Kemiskinan), and Per Capita Expenditure data from 2015-2024 using Fuzzy C-Means and OPTICS algorithms.

## 🌟 Features

### Clustering Algorithms
- **Fuzzy C-Means (FCM)**: Provides membership degrees for each data point across clusters
- **OPTICS**: Density-based clustering that can find arbitrary-shaped clusters and handle noise

### Visualizations
- **Interactive Scatter Plots**: Customizable axis selection for exploring relationships
- **Box Plots**: Statistical distribution analysis per cluster
- **Interactive Maps**: Geographic visualization using Leaflet with cluster coloring
- **Evaluation Metrics**: Davies-Bouldin Index and Silhouette Score

### Data Analysis
- **Multi-year Analysis**: Support for data from 2015-2024
- **Year Filtering**: Analyze specific years or all years combined
- **Export Options**: CSV, JSON, and comprehensive reports
- **Real-time Processing**: Live clustering with parameter adjustment

## 🏗️ Architecture

### Backend (Django)
- **Framework**: Django 5.2.5 with Django REST Framework
- **Clustering**: scikit-fuzzy, scikit-learn
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly
- **Geographic**: geopandas, folium

### Frontend (Vue.js)
- **Framework**: Vue 3 with Composition API
- **Routing**: Vue Router 4
- **Charts**: Chart.js with vue-chartjs
- **Maps**: Leaflet with vue-leaflet
- **HTTP Client**: Axios
- **Build Tool**: Vite

## 📊 Data Structure

The application expects CSV files with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `kabupaten_kota` | District/City name | Jakarta Pusat |
| `provinsi` | Province name | DKI Jakarta |
| `tahun` | Year (2015-2024) | 2023 |
| `ipm` | Human Development Index | 75.5 |
| `garis_kemiskinan` | Poverty line (IDR) | 532000 |
| `pengeluaran_per_kapita` | Per capita expenditure (IDR) | 8500000 |
| `latitude` | Latitude coordinate | -6.1745 |
| `longitude` | Longitude coordinate | 106.8227 |

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd fuzzy-clustering-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## 📈 Usage

### 1. Upload Dataset
- Navigate to the Upload page
- Choose between FCM or OPTICS algorithm
- Upload your CSV file or use the sample data
- Configure algorithm parameters:
  - **FCM**: Number of clusters, fuzzy coefficient, max iterations, tolerance
  - **OPTICS**: Min samples, xi parameter, min cluster size

### 2. View Results
- **Summary**: Total regions, clusters, execution time, iterations
- **Evaluation Metrics**: Davies-Bouldin Index and Silhouette Score with quality indicators
- **Visualizations**: 
  - Scatter plots with customizable axes
  - Box plots for statistical analysis
  - Interactive map with cluster coloring
- **Cluster Details**: Detailed information about each cluster and its members

### 3. Year Analysis
- Filter by specific years (2015-2024)
- Compare temporal changes in clustering patterns
- Analyze development trends over time

### 4. Export Results
- Export to CSV for further analysis
- Download JSON format for programmatic use
- Generate comprehensive text reports

## 🔧 API Endpoints

### Clustering Operations
- `POST /api/clustering/upload/` - Upload dataset and run clustering
- `GET /api/clustering/results/{session_id}/` - Get clustering results
- `GET /api/clustering/status/{session_id}/` - Check processing status

### Data Management
- `POST /api/clustering/validate/` - Validate dataset format
- `GET /api/clustering/years/{session_id}/` - Get available years
- `POST /api/clustering/rerun/{session_id}/` - Rerun with different parameters

### Export & Analysis
- `GET /api/clustering/export/{session_id}/` - Export results
- `GET /api/clustering/cluster/{session_id}/{cluster_id}/` - Cluster details
- `POST /api/clustering/report/{session_id}/` - Generate reports

## 📊 Sample Data

The application includes sample data for 30 major Indonesian cities from 2015-2024 with:
- Human Development Index values
- Poverty line figures
- Per capita expenditure data
- Geographic coordinates for mapping

## 🎯 Clustering Algorithms

### Fuzzy C-Means (FCM)
- **Advantages**: Handles overlapping clusters, provides uncertainty information
- **Parameters**: 
  - Number of clusters (2-10)
  - Fuzzy coefficient (1.1-5.0)
  - Max iterations (50-1000)
  - Tolerance (0.0001-0.1)

### OPTICS
- **Advantages**: Finds arbitrary-shaped clusters, handles noise automatically
- **Parameters**:
  - Min samples (2-50)
  - Xi parameter (0.01-1.0)
  - Min cluster size (0.01-0.5)

## 📏 Evaluation Metrics

### Davies-Bouldin Index
- **Range**: 0 to ∞ (lower is better)
- **Quality Indicators**:
  - < 1.0: Excellent
  - 1.0-1.5: Good
  - 1.5-2.0: Fair
  - > 2.0: Needs improvement

### Silhouette Score
- **Range**: -1 to 1 (higher is better)
- **Quality Indicators**:
  - > 0.7: Excellent
  - 0.5-0.7: Good
  - 0.25-0.5: Fair
  - < 0.25: Needs improvement

## 🗂️ Project Structure

```
├── backend/
│   ├── backend/           # Django project settings
│   ├── clustering/        # Main clustering app
│   │   ├── algorithms.py  # FCM and OPTICS implementations
│   │   ├── models.py      # Database models
│   │   ├── views.py       # API endpoints
│   │   └── urls.py        # URL routing
│   ├── requirements.txt   # Python dependencies
│   └── sample_data_indonesia.csv  # Sample dataset
├── fuzzy-clustering-frontend/
│   ├── src/
│   │   ├── components/    # Vue components
│   │   │   ├── ScatterPlot.vue
│   │   │   ├── BoxPlot.vue
│   │   │   └── InteractiveMap.vue
│   │   ├── views/         # Page components
│   │   │   ├── Home.vue
│   │   │   ├── UploadEnhanced.vue
│   │   │   └── AnalysisEnhanced.vue
│   │   ├── services/      # API services
│   │   └── router/        # Vue Router configuration
│   ├── package.json       # Node.js dependencies
│   └── vite.config.js     # Vite configuration
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the ISC License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Indonesian Central Statistics Agency (BPS) for data structure reference
- scikit-learn and scikit-fuzzy communities for algorithm implementations
- Vue.js and Django communities for excellent documentation
- Leaflet and Chart.js for visualization capabilities

## 📞 Support

For questions, issues, or contributions, please:
1. Check the existing issues on GitHub
2. Create a new issue with detailed description
3. Include sample data and error messages when reporting bugs

---

**Note**: This application is designed for research and educational purposes. Ensure you have proper permissions for any real-world data analysis.