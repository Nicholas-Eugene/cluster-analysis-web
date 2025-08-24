# Frontend Clustering Fuzzy C-Means

Frontend aplikasi web berbasis Vue.js untuk analisis clustering Fuzzy C-Means pada data profil kemiskinan kabupaten/kota di Indonesia berdasarkan IPM (Indeks Pembangunan Manusia) dan Garis Kemiskinan.

## 📋 Deskripsi

Aplikasi ini menyediakan interface yang user-friendly untuk:
- Upload dataset CSV dengan data IPM dan Garis Kemiskinan
- Konfigurasi parameter clustering Fuzzy C-Means
- Visualisasi hasil clustering dalam bentuk peta interaktif, scatter plot, dan dashboard
- Analisis detail setiap cluster dan evaluasi kualitas clustering
- Export hasil dalam berbagai format

## 🚀 Fitur Utama

### 1. Halaman Utama (Home)
- **Deskripsi lengkap** tentang algoritma Fuzzy C-Means
- **Latar belakang penelitian** dan tujuan analisis
- **Tahapan algoritma** dan keunggulan FCM
- **Informasi data** yang dianalisis (IPM dan Garis Kemiskinan)

### 2. Halaman Unggah Dataset (Upload)
- **Upload file CSV** dengan validasi format dan ukuran
- **Preview data** untuk memverifikasi struktur dataset
- **Konfigurasi parameter clustering:**
  - Jumlah cluster (2-10)
  - Fuzzy coefficient (1.1-5.0)
  - Maksimal iterasi (50-1000)
  - Toleransi error (0.0001-0.1)
  - Filter tahun (opsional)
- **Template dataset** yang dapat didownload
- **Validasi real-time** untuk memastikan data sesuai format

### 3. Halaman Analisis & Visualisasi (Analysis)
- **Dashboard komprehensif** dengan:
  - Ringkasan statistik clustering
  - Metrik evaluasi (Davies-Bouldin Index, Silhouette Score)
  - Peta interaktif Indonesia dengan hasil clustering
  - Scatter plot IPM vs Garis Kemiskinan
  - Analisis detail setiap cluster
  - Karakteristik dan profil setiap cluster
- **Export hasil** dalam format CSV, JSON, PNG, dan PDF

## 🛠️ Teknologi yang Digunakan

- **Vue.js 3** - Frontend framework dengan Composition API
- **Vue Router 4** - Routing dan navigasi
- **Axios** - HTTP client untuk komunikasi dengan backend
- **Chart.js + Vue-Chart.js** - Library untuk visualisasi grafik
- **Leaflet + Vue-Leaflet** - Library untuk peta interaktif
- **Vite** - Build tool dan development server

## 📦 Instalasi dan Setup

### Prasyarat
- Node.js (versi 16+)
- NPM atau Yarn
- Backend Django API (terpisah)

### Langkah Instalasi

1. **Masuk ke direktori project:**
```bash
cd fuzzy-clustering-frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Setup environment variables:**
Copy file `.env` yang sudah ada atau sesuaikan dengan backend Anda:
```bash
VUE_APP_API_URL=http://localhost:8000/api
```

4. **Jalankan development server:**
```bash
npm run dev
```

5. **Akses aplikasi:**
Buka browser dan akses `http://localhost:5173` (port default Vite)

## 🔧 Scripts Available

```bash
# Development server
npm run dev

# Build untuk production
npm run build

# Preview build hasil
npm run preview

# Serve production build
npm run serve
```

## 📁 Struktur Project

```
fuzzy-clustering-frontend/
├── public/
│   └── vite.svg
├── src/
│   ├── assets/
│   │   └── css/
│   │       └── global.css       # Global styling
│   ├── components/              # Reusable components
│   ├── services/
│   │   └── apiService.js        # API communication service
│   ├── views/
│   │   ├── Home.vue            # Halaman utama
│   │   ├── Upload.vue          # Halaman upload dataset
│   │   └── Analysis.vue        # Halaman analisis & visualisasi
│   ├── router/
│   │   └── index.js            # Vue Router configuration
│   ├── App.vue                 # Root component
│   └── main.js                 # Application entry point
├── index.html                  # HTML template
├── vite.config.js             # Vite configuration
├── package.json               # Dependencies & scripts
├── .env                       # Environment variables
├── .gitignore                 # Git ignore rules
└── README.md                  # Dokumentasi
```

## 🔗 Integrasi dengan Backend

Aplikasi ini dirancang untuk berkomunikasi dengan backend Django melalui REST API. Berikut endpoint yang digunakan:

### Upload & Processing
- `POST /api/clustering/upload/` - Upload dataset dan proses clustering
- `GET /api/clustering/status/{sessionId}/` - Cek status processing
- `POST /api/clustering/validate/` - Validasi format dataset

### Results & Analysis
- `GET /api/clustering/results/{sessionId}/` - Ambil hasil clustering
- `GET /api/clustering/cluster/{sessionId}/{clusterId}/` - Detail cluster tertentu
- `GET /api/clustering/evaluation/{sessionId}/` - Metrik evaluasi detail

### Export & Reports
- `GET /api/clustering/export/{sessionId}/?format=csv` - Export hasil
- `POST /api/clustering/report/{sessionId}/` - Generate report PDF

### Utility
- `GET /api/clustering/years/{sessionId}/` - Daftar tahun tersedia
- `DELETE /api/clustering/session/{sessionId}/` - Hapus session

## 📊 Format Dataset

Dataset yang diunggah harus berformat CSV dengan struktur sebagai berikut:

```csv
kabupaten_kota,tahun,ipm,garis_kemiskinan
Jakarta Pusat,2023,82.5,532000
Jakarta Utara,2023,78.2,548000
Bandung,2023,75.2,485000
...
```

### Kolom Wajib:
- **kabupaten_kota**: Nama kabupaten/kota
- **tahun**: Tahun data
- **ipm**: Nilai Indeks Pembangunan Manusia (float)
- **garis_kemiskinan**: Nilai garis kemiskinan dalam Rupiah (integer)

### Persyaratan:
- Format file: CSV (.csv)
- Encoding: UTF-8
- Delimiter: koma (,)
- Maksimal ukuran: 10 MB
- Minimal 2 baris (header + data)

## 🎨 Styling dan UI/UX

### Design System
- **Color Palette**: Gradient purple-blue theme
- **Typography**: Segoe UI font family
- **Components**: Card-based layout dengan shadow effects
- **Responsive**: Mobile-first design approach
- **Icons**: Unicode emoji untuk visual appeal

### Key Features:
- **Drag & drop** file upload interface
- **Real-time validation** dengan feedback visual
- **Interactive tooltips** untuk parameter clustering
- **Loading states** dan progress indicators
- **Responsive charts** dan visualizations
- **Accessible navigation** dengan clear hierarchy

## 🔍 Fitur Visualisasi

### 1. Peta Interaktif
- Menggunakan Leaflet.js untuk menampilkan peta Indonesia
- Marker berwarna sesuai cluster assignment
- Popup informatif untuk setiap wilayah
- Legend dinamis untuk interpretasi warna

### 2. Scatter Plot
- Chart.js untuk plotting IPM vs Garis Kemiskinan
- Point styling berdasarkan cluster
- Filter berdasarkan tahun
- Interactive tooltips dengan detail data

### 3. Dashboard Metrics
- Cards dengan statistik ringkasan
- Evaluation metrics dengan interpretasi
- Progress bars untuk membership degree
- Cluster characteristics analysis

## 🚀 Deployment

### Build untuk Production
```bash
npm run build
```

### Deploy ke Static Hosting
File hasil build di folder `dist/` dapat di-deploy ke:
- Netlify
- Vercel
- GitHub Pages
- Firebase Hosting
- CDN static hosting lainnya

### Environment Variables untuk Production
```bash
VUE_APP_API_URL=https://your-backend-api.com/api
```

## 📝 Troubleshooting

### Common Issues:

1. **"Missing script: dev" error:**
   - Pastikan package.json memiliki script "dev": "vite"
   - Jalankan `npm install` untuk install dependencies

2. **Port sudah digunakan:**
   - Vite akan otomatis mencari port yang tersedia
   - Atau specify port: `npm run dev -- --port 3000`

3. **Module import errors:**
   - Pastikan semua dependencies sudah terinstall
   - Check file extensions (.js) pada import statements

4. **Backend connection error:**
   - Pastikan backend Django sudah running
   - Check URL di file .env
   - Enable CORS di backend untuk frontend domain

## 🤝 Contributing

1. Fork project ini
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 License

Distributed under the ISC License.

## 📞 Support

Untuk pertanyaan atau dukungan teknis, silakan buat issue di repository ini.

---

**Catatan**: Aplikasi ini merupakan frontend yang memerlukan backend Django API untuk berfungsi penuh. Untuk development, tersedia mode demo dengan data sample yang dapat diakses melalui halaman Analysis.