# 🎭 Demo Guide - Frontend Clustering Fuzzy C-Means

## 🚀 Quick Start - Mode Mockup

Aplikasi sudah dikonfigurasi dalam **mode demo/mockup** sehingga Anda dapat melihat semua UI tanpa memerlukan backend Django.

### 1. Menjalankan Aplikasi

```bash
cd fuzzy-clustering-frontend
npm run dev
```

Aplikasi akan berjalan di: **http://localhost:5173**

### 2. Fitur Yang Dapat Dilihat

#### 🏠 **Halaman Utama** (`/`)
- **Tampilan lengkap** tentang algoritma Fuzzy C-Means
- **Hero section** dengan animasi interaktif
- **Penjelasan detail** tahapan algoritma
- **Latar belakang penelitian** dan data yang dianalisis
- **Navigation** responsif dengan gradient design

#### 📤 **Halaman Upload** (`/upload`) 
- **Drag & drop interface** untuk upload file CSV
- **Preview data otomatis** dengan data simulasi
- **Konfigurasi parameter FCM:**
  - Jumlah cluster (2-10)
  - Fuzzy coefficient (1.1-5.0) 
  - Maksimal iterasi (50-1000)
  - Toleransi error (0.0001-0.1)
- **Template dataset** yang bisa didownload
- **Tombol "Langsung ke Demo Hasil"** untuk skip ke visualisasi
- **Mode demo notice** di bagian atas

#### 📊 **Halaman Analisis** (`/analysis`)
- **Dashboard komprehensif** dengan data Indonesia simulasi
- **Ringkasan statistik** clustering (34 kab/kota, 3 cluster)
- **Metrik evaluasi** dengan interpretasi:
  - Davies-Bouldin Index: 0.8234 (Baik)
  - Silhouette Score: 0.6789 (Baik)
- **Peta interaktif Indonesia** dengan marker cluster berwarna
- **Scatter plot** IPM vs Garis Kemiskinan (Chart.js)
- **Analisis detail cluster** dengan:
  - Membership degree visualization
  - Tabel anggota cluster
  - Karakteristik setiap cluster
- **Export functionality** (CSV, JSON, PNG charts)

### 3. Data Demo Yang Ditampilkan

#### **Cluster 1** (Pembangunan Tinggi)
- Jakarta Pusat, Jakarta Selatan, Surabaya, Yogyakarta, Denpasar
- **IPM**: 76.8 - 84.1 
- **Garis Kemiskinan**: Rp 465,000 - Rp 580,000

#### **Cluster 2** (Pembangunan Sedang)  
- Bandung, Semarang, Makassar, Malang, Bekasi, Depok
- **IPM**: 72.8 - 76.1
- **Garis Kemiskinan**: Rp 380,000 - Rp 510,000

#### **Cluster 3** (Pembangunan Rendah)
- Medan, Banjarmasin, Pontianak, Mataram, Palu, Kupang, dll
- **IPM**: 65.4 - 75.8
- **Garis Kemiskinan**: Rp 295,000 - Rp 485,000

### 4. Flow Penggunaan Demo

1. **Start** di halaman utama (`/`)
2. **Klik** "Mulai Analisis" atau navigation "Unggah Dataset"
3. **Upload** file apapun (akan diterima dalam mode demo)
4. **Konfigurasi** parameter sesuai keinginan
5. **Klik** "Mulai Clustering (Demo)" atau "Langsung ke Demo Hasil"
6. **Lihat** hasil visualisasi lengkap di halaman analisis
7. **Test** semua fitur interaktif:
   - Switch antar cluster tabs
   - Filter tahun di scatter plot
   - Hover di peta dan chart
   - Export hasil dalam berbagai format

### 5. URL Yang Tersedia

- **`/`** - Halaman Utama
- **`/upload`** - Upload Dataset (Mode Mockup)
- **`/analysis`** - Analisis & Visualisasi (Mode Mockup)
- **`/upload-simple`** - Upload Sederhana (untuk testing)
- **`/upload-full`** - Upload Lengkap (untuk production dengan backend)
- **`/analysis-full`** - Analisis Lengkap (untuk production dengan backend)

### 6. Responsive Design Testing

Test tampilan di berbagai ukuran layar:
- **Desktop**: Layout 3-column grid optimal
- **Tablet**: Layout 2-column responsive
- **Mobile**: Single column dengan navigation collapsible

### 7. Browser Compatibility

Sudah ditest pada:
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

### 8. Performance Notes

- **Build size**: ~518KB gzipped (~176KB compressed)
- **Load time**: < 2 detik di koneksi cepat
- **Interactive elements**: Smooth 60fps animations
- **Charts**: Hardware accelerated dengan Canvas

## 🔧 Development Commands

```bash
# Development server (mode mockup)
npm run dev

# Production build
npm run build

# Preview production build
npm run preview

# Serve production build di port 3000
npm run serve
```

## 🎯 Features Showcase

### ✅ **Yang Sudah Berfungsi Penuh:**
- ✅ Responsive navigation dengan 3 halaman
- ✅ Upload interface dengan drag & drop
- ✅ Parameter configuration dengan validation
- ✅ Data preview dengan sample data Indonesia
- ✅ Interactive map dengan Leaflet.js
- ✅ Scatter plot dengan Chart.js
- ✅ Dashboard metrics dengan interpretasi
- ✅ Cluster analysis dengan membership visualization
- ✅ Export functionality (CSV, JSON, PNG)
- ✅ Modern gradient design dengan smooth animations
- ✅ Loading states dan error handling
- ✅ Tooltips dan help text
- ✅ Template dataset download

### 🔄 **Mode Transisi ke Production:**
Ketika backend Django sudah siap, tinggal:
1. Update router untuk menggunakan komponen original (`Upload.vue`, `Analysis.vue`)
2. Set environment variable `VUE_APP_API_URL`
3. Remove mockup notice dari UI

## 📱 Demo Screenshots Path

Untuk dokumentasi, Anda bisa screenshot:
1. **Halaman Utama**: Hero section + algoritma explanation
2. **Upload Page**: Drag & drop + parameter config
3. **Analysis Dashboard**: Metrics + map + scatter plot
4. **Cluster Details**: Membership table + characteristics
5. **Mobile View**: Responsive design

---

**🎉 Aplikasi siap untuk demo presentasi!** Semua fitur UI sudah functional dengan data Indonesia yang realistis.