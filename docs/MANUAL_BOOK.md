# 📖 Manual Book - Fuzzy Clustering Analysis System

**Aplikasi Analisis Clustering Wilayah Indonesia**  
**Version:** 1.0  
**Last Updated:** October 2025

---

## Daftar Isi

1. [Pengenalan Aplikasi](#1-pengenalan-aplikasi)
2. [Instalasi & Setup](#2-instalasi--setup)
3. [Panduan Penggunaan](#3-panduan-penggunaan)
4. [Fitur-Fitur Utama](#4-fitur-fitur-utama)
5. [Interpretasi Hasil](#5-interpretasi-hasil)
6. [Troubleshooting](#6-troubleshooting)
7. [FAQ](#7-faq)

---

## 1. Pengenalan Aplikasi

### 1.1 Tentang Aplikasi

**Fuzzy Clustering Analysis System** adalah aplikasi web untuk menganalisis karakteristik wilayah Indonesia berdasarkan indikator pembangunan menggunakan algoritma machine learning.

**Tujuan:**
- Mengelompokkan 514 kabupaten/kota di Indonesia berdasarkan kesamaan karakteristik
- Mengidentifikasi pola pembangunan regional
- Memberikan interpretasi otomatis untuk setiap cluster

**Indikator yang Dianalisis:**
- **IPM** (Indeks Pembangunan Manusia)
- **Garis Kemiskinan** (Rupiah/bulan)
- **Pengeluaran Per Kapita** (Rupiah/tahun)

---

### 1.2 Algoritma yang Tersedia

#### A. Fuzzy C-Means (FCM)
**Karakteristik:**
- Soft clustering (setiap data memiliki derajat keanggotaan ke semua cluster)
- User menentukan jumlah cluster (2-10)
- Cocok untuk data dengan batas cluster yang fuzzy/tidak tegas

**Kapan Menggunakan:**
- Ketika jumlah cluster sudah diketahui
- Data memiliki overlap antar kelompok
- Ingin mengetahui tingkat keanggotaan (membership degree)

#### B. OPTICS
**Karakteristik:**
- Density-based clustering
- Otomatis menentukan jumlah cluster
- Dapat mendeteksi noise/outlier

**Kapan Menggunakan:**
- Tidak tahu berapa jumlah cluster yang optimal
- Ingin mendeteksi outlier
- Data memiliki variasi densitas

---

### 1.3 Mode Analisis

#### Mode 1: Per Tahun (Default)
- Clustering dilakukan terpisah untuk setiap tahun
- Dapat melacak perubahan cluster dari tahun ke tahun
- Cocok untuk analisis tren temporal

**Contoh Output:**
- Clustering tahun 2016
- Clustering tahun 2017
- Clustering tahun 2018
- dst.

#### Mode 2: Semua Tahun Sekaligus
- Semua data dari semua tahun di-cluster sekaligus
- Menghasilkan satu set cluster untuk semua tahun
- Cocok untuk melihat pola umum

**Contoh Output:**
- Clustering gabungan 2016-2023

---

## 2. Instalasi & Setup

### 2.1 Kebutuhan Sistem

**Minimum Requirements:**
- **Browser:** Chrome 90+, Firefox 88+, Edge 90+, Safari 14+
- **RAM:** 4 GB (8 GB recommended)
- **Koneksi Internet:** Diperlukan untuk akses aplikasi
- **Screen Resolution:** 1366x768 minimum

**Untuk Development/Local Installation:**
- **Python:** 3.8 atau lebih tinggi
- **Node.js:** 16.x atau lebih tinggi
- **npm:** 7.x atau lebih tinggi
- **Storage:** 2 GB free space

---

### 2.2 Instalasi (untuk Developer)

#### Windows:
```bash
# 1. Download atau clone repository
git clone <repository-url>
cd cluster-analysis-web

# 2. Jalankan setup script
setup.bat

# 3. Akses aplikasi
Browser: http://localhost:5173 (Frontend)
API: http://localhost:8000 (Backend)
```

#### Linux/Mac:
```bash
# 1. Download atau clone repository
git clone <repository-url>
cd cluster-analysis-web

# 2. Beri permission dan jalankan setup
chmod +x setup.sh
./setup.sh

# 3. Akses aplikasi
Browser: http://localhost:5173 (Frontend)
API: http://localhost:8000 (Backend)
```

#### Manual Installation:

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend:**
```bash
cd fuzzy-clustering-frontend
npm install
npm run dev
```

---

### 2.3 Akses Aplikasi

**URL:** `http://localhost:5173`  
**Status Check:** Pastikan halaman home terbuka dengan judul "Analisis Clustering Regional Indonesia"

---

## 3. Panduan Penggunaan

### 3.1 Persiapan Data

#### Format File yang Diterima:
- **CSV** (.csv) - UTF-8 encoding, comma delimiter
- **Excel** (.xlsx, .xls)
- **Ukuran Maksimal:** 10 MB

#### Struktur Data:

**5 Kolom Wajib:**

| Kolom | Deskripsi | Contoh | Wajib |
|-------|-----------|--------|-------|
| `kabupaten_kota` | Nama kabupaten/kota | Jakarta Pusat | ✅ |
| `tahun` | Tahun data | 2016, 2017, 2018 | ✅ |
| `ipm` | Nilai IPM | 75.5 | ✅ |
| `garis_kemiskinan` | Garis kemiskinan (Rp) | 532000 | ✅ |
| `pengeluaran_per_kapita` | Pengeluaran per kapita (Rp) | 8500000 | ✅ |

**Contoh Data:**

```csv
kabupaten_kota,tahun,ipm,garis_kemiskinan,pengeluaran_per_kapita
Jakarta Pusat,2016,80.5,532000,12500000
Jakarta Pusat,2017,81.2,545000,13000000
Jakarta Selatan,2016,79.8,528000,11800000
Surabaya,2016,78.3,420000,9500000
Bandung,2016,77.5,410000,8900000
```

**Catatan Penting:**
- ✅ Header kolom harus ada di baris pertama
- ✅ Tidak boleh ada cell kosong
- ✅ Nama kolom tidak case-sensitive (bisa `IPM`, `ipm`, atau `Ipm`)
- ✅ Satu kabupaten/kota dapat memiliki data untuk beberapa tahun

---

### 3.2 Langkah-Langkah Penggunaan

#### Langkah 1: Upload File

1. **Buka halaman Upload**
   - Klik menu "Upload" atau akses langsung dari home page
   
2. **Pilih File**
   - **Metode 1:** Klik area "Klik atau drag & drop file"
   - **Metode 2:** Drag & drop file ke area upload
   - **Metode 3:** Gunakan "Data Sample" untuk testing

3. **Verifikasi Preview**
   - Sistem akan menampilkan preview data
   - Periksa:
     - ✅ Total baris sesuai
     - ✅ Kolom terdeteksi dengan benar
     - ✅ Tahun terdeteksi
     - ✅ Sample data benar

**Screenshot Area:**
```
┌─────────────────────────────────────┐
│  📁 Klik atau drag & drop file CSV  │
│      atau Excel di sini             │
│                                     │
│  Format: .csv, .xlsx | Max: 10 MB   │
└─────────────────────────────────────┘
```

---

#### Langkah 2: Pilih Mode Clustering

**Lokasi:** Bagian "Konfigurasi Parameter"

**Pilihan:**

**A. Per Tahun (Default) - Recommended**
```
Mode Clustering: [Per Tahun ▼]

Pilih Tahun untuk Di-cluster:
[✓] 2016  [✓] 2017  [✓] 2018  [✓] 2019  [✓] 2020

Tahun yang dipilih (5): 2016, 2017, 2018, 2019, 2020
```

**Kapan menggunakan:**
- Ingin melihat pola per tahun
- Analisis tren temporal
- Membandingkan hasil antar tahun

**B. Semua Tahun Sekaligus**
```
Mode Clustering: [Semua Tahun Sekaligus ▼]
```

**Kapan menggunakan:**
- Ingin clustering semua data sekaligus
- Melihat pola umum tanpa mempertimbangkan tahun

---

#### Langkah 3: Pilih Algoritma

**Lokasi:** Bagian "Pilih Algoritma Clustering"

**Pilihan:**

**A. Fuzzy C-Means (FCM)**

```
┌──────────────────────────────────┐
│ ✓ Fuzzy C-Means (FCM)            │
│                                  │
│ Soft clustering dengan derajat   │
│ keanggotaan fuzzy                │
│                                  │
│ ✓ User menentukan jumlah cluster │
│ ✓ Membership degree              │
│ ✓ Iterative optimization         │
└──────────────────────────────────┘
```

**Parameter:**
- **Jumlah Cluster:** 2-10 (default: 3)
- **Fuzzy Coefficient:** 1.1-5.0 (default: 2.0)
- **Max Iterations:** 100-1000 (default: 300)
- **Tolerance:** 0.0001-0.01 (default: 0.0001)

**Rekomendasi:**
- Cluster 3: Daerah Maju, Berkembang, Tertinggal
- Cluster 4-5: Analisis lebih detail
- Fuzzy Coeff 2.0: Standard, balanced
- Fuzzy Coeff > 2.5: Lebih fuzzy/overlap

**B. OPTICS**

```
┌──────────────────────────────────┐
│ ✓ OPTICS                         │
│                                  │
│ Density-based clustering dengan  │
│ deteksi noise otomatis           │
│                                  │
│ ✓ Otomatis tentukan jumlah       │
│ ✓ Deteksi outlier                │
│ ✓ Variasi densitas               │
└──────────────────────────────────┘
```

**Parameter:**
- **Min Samples:** 2-50 (default: 5)
- **Xi:** 0.01-1.0 (default: 0.05)
- **Min Cluster Size:** 0.01-0.5 (default: 0.05)

**Rekomendasi:**
- Min Samples 5: Standard
- Min Samples 10-15: Data banyak
- Xi 0.05: Standard sensitivity
- Xi < 0.05: Lebih sensitif (lebih banyak cluster)

---

#### Langkah 4: Konfigurasi Parameter (FCM)

**Jika memilih FCM:**

1. **Jumlah Cluster**
   ```
   Jumlah Cluster: [3] (slider 2-10)
   ```
   - 2-3 cluster: Klasifikasi sederhana
   - 4-6 cluster: Analisis detail
   - 7-10 cluster: Sangat detail (bisa overfit)

2. **Fuzzy Coefficient (m)**
   ```
   Fuzzy Coefficient: [2.0] (slider 1.1-5.0)
   ```
   - 1.1-1.5: Mendekati hard clustering
   - 2.0: Standard (recommended)
   - 2.5-5.0: Very fuzzy, banyak overlap

3. **Max Iterations**
   ```
   Max Iterations: [300]
   ```
   - Default 300 sudah cukup
   - Tingkatkan jika tidak konvergen

4. **Tolerance**
   ```
   Tolerance: [0.0001]
   ```
   - Default 0.0001 recommended
   - Lebih kecil = lebih presisi tapi lambat

---

#### Langkah 5: Konfigurasi Parameter (OPTICS)

**Jika memilih OPTICS:**

1. **Minimum Samples**
   ```
   Min Samples: [5] (slider 2-50)
   ```
   - 2-5: Data sedikit atau cluster kecil
   - 5-10: Standard
   - 10-20: Data banyak, cluster besar

2. **Xi Parameter**
   ```
   Xi: [0.05] (slider 0.01-1.0)
   ```
   - 0.01-0.03: Sangat sensitif
   - 0.05: Standard
   - 0.1-0.3: Kurang sensitif

3. **Min Cluster Size**
   ```
   Min Cluster Size: [0.05] (5%)
   ```
   - 0.01-0.03: Cluster sangat kecil OK
   - 0.05: Standard (5% dari data)
   - 0.1-0.2: Cluster harus besar

---

#### Langkah 6: Proses Clustering

1. **Verifikasi Semua Input**
   - ✅ File ter-upload
   - ✅ Mode dipilih
   - ✅ Tahun dipilih (jika per tahun)
   - ✅ Algoritma dipilih
   - ✅ Parameter dikonfigurasi

2. **Klik "Mulai Clustering FCM" atau "Mulai Clustering OPTICS"**
   ```
   [⚙️ Mulai Clustering FCM]
   ```

3. **Tunggu Proses**
   - Indikator loading akan muncul
   - "Memproses..." ditampilkan
   - Waktu: 3-30 detik tergantung data

4. **Redirect Otomatis**
   - Sistem akan redirect ke halaman Analysis
   - Hasil clustering ditampilkan

**Pesan Sukses:**
```
✅ Dataset berhasil diproses!
```

---

### 3.3 Memahami Hasil

#### A. Ringkasan Clustering (Summary)

**Informasi yang Ditampilkan:**

```
┌────────────────────────────────────┐
│ 📊 Ringkasan Clustering            │
├────────────────────────────────────┤
│ Jumlah Cluster: 3                  │
│ Total Wilayah: 34                  │
│ Algoritma: FCM                     │
│ Iterasi: 42                        │
│ Waktu Eksekusi: 2.34 detik         │
├────────────────────────────────────┤
│ 📈 Metrik Kualitas                 │
├────────────────────────────────────┤
│ Davies-Bouldin: 0.8234             │
│ Silhouette Score: 0.6789           │
└────────────────────────────────────┘
```

**Interpretasi Metrik:**

**Davies-Bouldin Index:**
- < 1.0: **Excellent** - Cluster sangat terpisah
- 1.0-1.5: **Good** - Cluster cukup terpisah
- 1.5-2.0: **Fair** - Cluster kurang terpisah
- > 2.0: **Poor** - Cluster overlap banyak

**Silhouette Score:**
- 0.7-1.0: **Excellent** - Cluster sangat baik
- 0.5-0.7: **Good** - Cluster baik
- 0.25-0.5: **Fair** - Struktur cluster ada
- < 0.25: **Poor** - Cluster lemah

---

#### B. Detail Cluster

**Untuk setiap cluster, ditampilkan:**

**1. Label & Interpretasi Otomatis**
```
Cluster 0: Daerah Maju Biaya Tinggi
Ukuran: 15 wilayah
```

**Kategori Interpretasi:**
- 🏆 **Daerah Maju Biaya Tinggi** - IPM tinggi, biaya tinggi
- 💰 **Daerah Maju Biaya Rendah** - IPM tinggi, biaya rendah
- 📈 **Daerah Berkembang Potensial** - IPM sedang, pengeluaran tinggi
- 🎯 **Daerah Berkembang Stabil** - IPM sedang, biaya sedang
- ⚠️ **Daerah Berkembang Tertantang** - IPM sedang, biaya tinggi
- 📉 **Daerah Tertinggal Berat** - IPM rendah, biaya rendah
- 🆘 **Daerah Tertinggal Sangat Berat** - IPM rendah, biaya tinggi
- ❓ **Daerah Karakteristik Campuran** - Karakteristik mixed

**2. Karakteristik (Centroid)**
```
IPM: 75.24
Garis Kemiskinan: Rp 450,000/bulan
Pengeluaran Per Kapita: Rp 12,500,000/tahun
```

**3. Anggota Cluster**
```
Wilayah dalam cluster ini (15):
Jakarta Pusat, Jakarta Selatan, Surabaya, 
Bandung, Semarang, Yogyakarta, Malang, 
Denpasar, Makassar, Palembang, Medan, 
Pekanbaru, Balikpapan, Manado, Pontianak
```

---

#### C. Visualisasi

**1. Scatter Plot**
- **Sumbu X:** IPM
- **Sumbu Y:** Garis Kemiskinan
- **Warna:** Cluster berbeda
- **Ukuran:** Proporsi data

**Cara Membaca:**
- Titik berwarna sama = cluster yang sama
- Titik mengelompok = cluster kohesif
- Titik tersebar = cluster kurang jelas
- Overlap = fuzzy boundary

**2. Box Plot**
- **Distribusi** setiap metrik per cluster
- **Median** (garis tengah box)
- **Q1-Q3** (box)
- **Min-Max** (whiskers)
- **Outlier** (titik di luar whisker)

**Cara Membaca:**
- Box tinggi = variasi tinggi
- Box pendek = variasi rendah
- Median berbeda = cluster terpisah
- Banyak outlier = data tidak homogen

**3. Silhouette Plot**
- **Lebar bar** = silhouette coefficient
- **Positif** = baik (dalam cluster yang tepat)
- **Negatif** = salah cluster
- **Garis merah** = rata-rata

**Cara Membaca:**
- Bar panjang (>0.5) = baik
- Bar pendek (<0.3) = kurang baik
- Bar negatif = salah cluster
- Cluster lebih lebar = lebih kohesif

**4. Correlation Heatmap**
- **Warna** = korelasi (-1 to 1)
- **Biru tua** = korelasi negatif kuat
- **Putih** = tidak berkorelasi
- **Ungu tua** = korelasi positif kuat

**Cara Membaca:**
- Diagonal selalu 1.0 (korelasi dengan diri sendiri)
- Positif = naik bersamaan
- Negatif = berlawanan arah

**5. Peta Geografis**
- **Titik berwarna** = wilayah per cluster
- **Warna** = cluster assignment
- **Lokasi** = koordinat geografis

**Cara Membaca:**
- Cluster mengelompok geografis = pola regional
- Cluster tersebar = tidak ada pola geografis
- Konsentrasi = hotspot karakteristik tertentu

---

### 3.4 Download PDF Report

**Lokasi:** Tombol "Download PDF Report" di halaman hasil

**Isi PDF Report:**

1. **Cover Page**
   - Judul report
   - Tanggal generate
   - Mode analisis
   - Algoritma used

2. **Summary**
   - Total wilayah
   - Jumlah cluster
   - Metrik kualitas
   - Parameter

3. **Visualisasi**
   - Peta geografis (jika ada koordinat)
   - Scatter plots (IPM vs Kemiskinan, dll)
   - Box plots
   - Correlation heatmap
   - Silhouette plot

4. **Detail Cluster**
   - Label interpretasi
   - Deskripsi karakteristik
   - Centroid values
   - **Semua anggota cluster** (comma-separated)

**Cara Download:**
1. Klik "📥 Download PDF Report"
2. Tunggu proses generate (5-15 detik)
3. PDF otomatis ter-download
4. Buka dengan PDF reader

**Ukuran File:** 0.8 - 2 MB  
**Halaman:** 10-30 halaman (tergantung jumlah cluster & tahun)

---

## 4. Fitur-Fitur Utama

### 4.1 Auto-Interpretation

**Fitur:** Sistem secara otomatis memberikan label dan deskripsi untuk setiap cluster

**Cara Kerja:**
1. Analisis centroid cluster (IPM, Garis Kemiskinan, Pengeluaran)
2. Bandingkan dengan threshold (rendah: <33%, sedang: 33-67%, tinggi: >67%)
3. Klasifikasi ke 8 kategori
4. Generate label dan deskripsi

**Contoh Output:**
```
Cluster 0: Daerah Maju Biaya Tinggi

Deskripsi: Daerah dengan IPM tinggi (75.24), pengeluaran 
per kapita tinggi (Rp 12,500,000/tahun), dan garis 
kemiskinan tinggi (Rp 450,000/bulan). Karakteristik kota 
besar dengan standar hidup tinggi.
```

---

### 4.2 Geographic Visualization

**Fitur:** Peta Indonesia dengan 495 kota yang ter-mapping koordinatnya

**Coverage:**
- ✅ 38 provinsi
- ✅ 495 kabupaten/kota (96% dari 514 total)
- ✅ Auto-mapping dari nama kota

**Cara Kerja:**
1. Sistem cari koordinat dari database 495 kota
2. Jika tidak ketemu, gunakan koordinat dari data (jika ada)
3. Plot di peta dengan warna sesuai cluster

**Benefit:**
- Lihat pola geografis clustering
- Identifikasi konsentrasi karakteristik regional
- Visual yang mudah dipahami

---

### 4.3 Per-Year Analysis

**Fitur:** Analisis clustering terpisah per tahun untuk tracking tren

**Cara Menggunakan:**
1. Pilih mode "Per Tahun"
2. Pilih tahun yang ingin dianalisis
3. Proses clustering
4. Lihat hasil per tahun

**Output:**
- Tab untuk setiap tahun
- Visualisasi per tahun
- Perbandingan metrik antar tahun

**Use Case:**
- Tracking perubahan cluster membership
- Analisis tren pembangunan
- Identifikasi wilayah yang naik/turun kategori

---

### 4.4 Comprehensive PDF Export

**Fitur:** Export hasil ke PDF dengan semua visualisasi dan detail

**Konten:**
- ✅ Semua chart & plot
- ✅ Peta geografis
- ✅ Detail semua cluster
- ✅ Semua anggota cluster
- ✅ Metrik kualitas
- ✅ Professional formatting

**Format:**
- A4 size
- High resolution (200 DPI)
- Color coding consistent
- Ready to print/present

---

## 5. Interpretasi Hasil

### 5.1 Memahami Kategori Cluster

#### 🏆 Daerah Maju Biaya Tinggi
**Karakteristik:**
- IPM: > 67th percentile (tinggi)
- Garis Kemiskinan: > 67th percentile (tinggi)
- Pengeluaran: > 67th percentile (tinggi)

**Contoh:** Jakarta, Surabaya, Bandung  
**Interpretasi:** Kota besar dengan ekonomi maju tapi biaya hidup tinggi  
**Policy Implication:** Fokus pada affordability & inequality

#### 💰 Daerah Maju Biaya Rendah
**Karakteristik:**
- IPM: > 67th percentile (tinggi)
- Garis Kemiskinan: < 33rd percentile (rendah)
- Pengeluaran: > 67th percentile (tinggi)

**Contoh:** Yogyakarta (beberapa kasus)  
**Interpretasi:** Daerah maju dengan biaya hidup terjangkau  
**Policy Implication:** Model ideal untuk dikembangkan

#### 📈 Daerah Berkembang Potensial
**Karakteristik:**
- IPM: 33-67th percentile (sedang)
- Pengeluaran: > 67th percentile (tinggi)

**Interpretasi:** Ekonomi tumbuh, IPM belum catching up  
**Policy Implication:** Fokus pada pendidikan & kesehatan

#### 🎯 Daerah Berkembang Stabil
**Karakteristik:**
- IPM: 33-67th percentile (sedang)
- Garis Kemiskinan: 33-67th percentile (sedang)
- Pengeluaran: 33-67th percentile (sedang)

**Interpretasi:** Kondisi stabil, balanced growth  
**Policy Implication:** Maintain & accelerate development

#### ⚠️ Daerah Berkembang Tertantang
**Karakteristik:**
- IPM: 33-67th percentile (sedang)
- Garis Kemiskinan: > 67th percentile (tinggi)
- Pengeluaran: < 33rd percentile (rendah)

**Interpretasi:** Kemiskinan tinggi meski IPM sedang  
**Policy Implication:** Targeted poverty alleviation

#### 📉 Daerah Tertinggal Berat
**Karakteristik:**
- IPM: < 33rd percentile (rendah)
- Garis Kemiskinan: < 33rd percentile (rendah)
- Pengeluaran: < 33rd percentile (rendah)

**Interpretasi:** Daerah tertinggal dengan kondisi ekonomi lemah  
**Policy Implication:** Comprehensive development intervention

#### 🆘 Daerah Tertinggal Sangat Berat
**Karakteristik:**
- IPM: < 33rd percentile (rendah)
- Garis Kemiskinan: > 67th percentile (tinggi)
- Pengeluaran: < 33rd percentile (rendah)

**Interpretasi:** Kondisi paling menantang  
**Policy Implication:** Priority development focus

#### ❓ Daerah Karakteristik Campuran
**Karakteristik:**
- Mixed pattern, tidak fit kategori lain

**Interpretasi:** Pola unik, perlu analisis detail  
**Policy Implication:** Customized approach

---

### 5.2 Metrik Kualitas Clustering

#### Davies-Bouldin Index

**Formula:** Rata-rata similarity antara cluster

**Interpretasi:**
- **< 0.5:** Excellent - Cluster sangat compact & separated
- **0.5-1.0:** Very Good - Cluster jelas terpisah
- **1.0-1.5:** Good - Clustering bagus
- **1.5-2.0:** Fair - Masih acceptable
- **> 2.0:** Poor - Cluster overlap banyak, pertimbangkan ulang parameter

**Action Based on Score:**
- **Poor (>2.0):** 
  - FCM: Kurangi jumlah cluster atau ubah fuzzy coefficient
  - OPTICS: Adjust min_samples atau xi
  
- **Good (<1.5):** Lanjutkan dengan analisis

#### Silhouette Score

**Formula:** Measure seberapa mirip objek dengan cluster-nya vs cluster lain

**Interpretasi:**
- **0.7-1.0:** Excellent - Strong structure
- **0.5-0.7:** Good - Reasonable structure
- **0.25-0.5:** Fair - Weak structure
- **< 0.25:** Poor - No substantial structure
- **Negatif:** Very Poor - Salah cluster

**Action Based on Score:**
- **Poor (<0.3):** Reconsider number of clusters
- **Good (>0.5):** Hasil dapat dipercaya

---

### 5.3 Tips Interpretasi Visual

#### Scatter Plot
```
Jika melihat:
✓ Cluster terpisah jelas → Good clustering
✓ Cluster overlap sedikit → Normal (fuzzy boundaries)
✗ Cluster tercampur total → Bad clustering

Action: 
- Overlap banyak → Adjust parameters
- Pola tidak jelas → Coba algoritma lain
```

#### Box Plot
```
Jika melihat:
✓ Median berbeda signifikan → Cluster distinct
✓ Box tidak overlap → Clear separation
✗ Box overlap banyak → Weak separation

Action:
- Box sangat overlap → Merge cluster atau adjust parameter
- Banyak outlier → Check data quality
```

#### Silhouette Plot
```
Jika melihat:
✓ Bar panjang & positif → Good assignment
✓ Ukuran cluster balance → Good distribution
✗ Bar negatif banyak → Many misclassified
✗ Satu cluster sangat dominan → Imbalanced

Action:
- Banyak negatif → Re-run dengan parameter berbeda
- Imbalanced → Adjust min_cluster_size (OPTICS) atau num_clusters (FCM)
```

---

## 6. Troubleshooting

### 6.1 Error Upload File

#### Error: "Kolom yang hilang: ..."
**Penyebab:** File tidak memiliki semua kolom wajib  
**Solusi:**
1. Pastikan 5 kolom ada: kabupaten_kota, tahun, ipm, garis_kemiskinan, pengeluaran_per_kapita
2. Cek spelling kolom (case-insensitive OK)
3. Pastikan header di baris pertama

#### Error: "File terlalu besar"
**Penyebab:** File > 10 MB  
**Solusi:**
1. Reduce jumlah tahun
2. Remove kolom tidak perlu
3. Compress file atau gunakan CSV instead of Excel

#### Error: "Format file tidak didukung"
**Penyebab:** File bukan CSV/Excel  
**Solusi:**
1. Konversi ke .csv atau .xlsx
2. Pastikan encoding UTF-8 (untuk CSV)

#### Error: "Gagal membaca file CSV"
**Penyebab:** Encoding atau delimiter salah  
**Solusi:**
1. Save as CSV dengan UTF-8 encoding
2. Pastikan delimiter koma (,)
3. Cek tidak ada koma dalam data

---

### 6.2 Error Processing

#### Error: "Silakan pilih minimal 1 tahun..."
**Penyebab:** Mode "Per Tahun" tapi tidak ada tahun dipilih  
**Solusi:**
1. Centang minimal 1 tahun
2. Atau klik "✓ Pilih Semua"
3. Atau ganti mode ke "Semua Tahun Sekaligus"

#### Error: "Jumlah cluster harus antara 2-10"
**Penyebab:** Parameter di luar range  
**Solusi:** Adjust slider ke range yang valid

#### Error: "Clustering gagal konvergen"
**Penyebab:** FCM tidak mencapai konvergensi  
**Solusi:**
1. Tingkatkan max_iter (500-1000)
2. Adjust tolerance (lebih besar, misal 0.001)
3. Coba fuzzy coefficient berbeda
4. Reduce jumlah cluster

#### Error: "Tidak ada cluster ditemukan" (OPTICS)
**Penyebab:** Parameter terlalu strict  
**Solusi:**
1. Kurangi min_samples (coba 3-5)
2. Tingkatkan xi (coba 0.1-0.2)
3. Kurangi min_cluster_size (coba 0.01-0.03)

---

### 6.3 Error Visualisasi

#### Grafik tidak muncul
**Penyebab:** Browser compatibility atau JavaScript error  
**Solusi:**
1. Refresh halaman (F5)
2. Clear browser cache (Ctrl+Shift+Del)
3. Gunakan browser modern (Chrome/Firefox/Edge)
4. Disable ad blocker

#### PDF tidak ter-download
**Penyebab:** Pop-up blocker atau server error  
**Solusi:**
1. Allow pop-ups untuk website ini
2. Tunggu lebih lama (large data butuh 10-20 detik)
3. Check browser download settings
4. Retry download

#### Peta tidak muncul di PDF
**Penyebab:** Tidak ada koordinat yang valid  
**Solusi:**
1. Normal jika data tidak punya koordinat
2. Sistem akan skip map section
3. Interpretasi tetap tersedia

---

### 6.4 Performance Issues

#### Upload sangat lambat
**Solusi:**
1. Check koneksi internet
2. Reduce file size
3. Gunakan CSV instead of Excel
4. Close aplikasi lain

#### Processing timeout
**Solusi:**
1. Reduce data size (pilih beberapa tahun saja)
2. Reduce max_iter
3. Gunakan fewer clusters
4. Retry saat server tidak sibuk

#### Browser freeze
**Solusi:**
1. Close tabs lain
2. Increase browser memory
3. Use incognito mode
4. Clear cache & cookies

---

## 7. FAQ

### 7.1 Umum

**Q: Apakah aplikasi ini gratis?**  
A: Ya, aplikasi ini gratis untuk digunakan.

**Q: Apakah data saya aman?**  
A: Data hanya disimpan sementara selama sesi. Tidak ada data yang disimpan permanen di server.

**Q: Berapa lama sesi berlaku?**  
A: Sesi berlaku selama aplikasi berjalan. Jika refresh, perlu upload ulang.

**Q: Bisa digunakan offline?**  
A: Tidak, aplikasi memerlukan koneksi internet untuk backend processing.

**Q: Support mobile?**  
A: Ya, aplikasi responsive tapi optimal di desktop/laptop.

---

### 7.2 Data

**Q: Berapa minimal data yang dibutuhkan?**  
A: Minimal 10-15 baris data untuk hasil yang meaningful.

**Q: Boleh ada data yang hilang?**  
A: Tidak, semua cell harus terisi. Data kosong akan di-reject.

**Q: Perlu data provinsi?**  
A: Tidak wajib. Provinsi hanya untuk display di hasil, tidak digunakan untuk clustering.

**Q: Format angka bagaimana?**  
A: 
- IPM: Desimal OK (75.5 atau 75,5)
- Rupiah: Tanpa titik/koma pemisah ribuan (532000 bukan 532.000)

**Q: Bisa data selain Indonesia?**  
A: Bisa, tapi interpretasi dan peta disesuaikan untuk Indonesia. Label cluster tetap generate.

---

### 7.3 Algoritma

**Q: FCM atau OPTICS, mana yang lebih baik?**  
A: Tergantung kebutuhan:
- FCM: Jika tahu jumlah cluster, ingin membership degree
- OPTICS: Jika explore optimal cluster, ingin deteksi outlier

**Q: Berapa jumlah cluster optimal?**  
A: 
- 3 cluster: Simple categorization (Maju, Berkembang, Tertinggal)
- 4-5 cluster: Balanced detail
- 6+ cluster: Risk of overfitting

**Q: Hasil clustering berbeda setiap run?**  
A: FCM ada random initialization, jadi bisa sedikit berbeda. OPTICS deterministik.

**Q: Apakah clustering = prediksi?**  
A: Tidak. Clustering adalah unsupervised learning untuk grouping. Bukan prediksi masa depan.

---

### 7.4 Hasil

**Q: Bagaimana jika silhouette score rendah?**  
A: 
1. Coba adjust parameter
2. Coba algoritma lain
3. Jika tetap rendah, mungkin data tidak punya struktur cluster yang jelas

**Q: Cluster noise (OPTICS) itu apa?**  
A: Data yang tidak fit ke cluster manapun. Bisa jadi outlier atau karakteristik unik.

**Q: Kenapa satu cluster sangat besar?**  
A: 
- Normal jika banyak daerah punya karakteristik mirip
- Atau parameter terlalu loose
- Coba increase jumlah cluster (FCM) atau adjust min_cluster_size (OPTICS)

**Q: Interpretasi cluster bisa salah?**  
A: Interpretasi otomatis berdasarkan threshold statistik. Selalu validasi dengan domain knowledge.

---

### 7.5 PDF Export

**Q: Berapa lama generate PDF?**  
A: 5-15 detik untuk data normal, bisa 20-30 detik untuk data besar.

**Q: PDF tidak muncul peta?**  
A: Normal jika data tidak punya koordinat valid. Interpretasi tetap ada.

**Q: Bisa customize PDF?**  
A: Saat ini tidak ada opsi customize. PDF otomatis include semua visualisasi.

**Q: Format PDF bisa diubah?**  
A: Saat ini hanya PDF. Future: Excel, CSV export.

---

## 8. Kontak & Support

### 8.1 Pelaporan Bug

Jika menemukan bug:
1. Screenshot error message
2. Catat steps yang dilakukan
3. Report via GitHub Issues atau email

### 8.2 Permintaan Fitur

Saran fitur baru? 
1. Check dokumentasi (mungkin sudah ada)
2. Submit feature request via GitHub
3. Jelaskan use case dan benefit

### 8.3 Dokumentasi Tambahan

- **Technical Documentation:** `/docs/README.md`
- **API Documentation:** `/docs/API_DOCUMENTATION.md`
- **Setup Guide:** `/docs/SETUP_GUIDE.md`
- **Development Guide:** `/docs/CLEAN_CODE_GUIDE.md`

---

## Lampiran

### A. Contoh Dataset

Download sample dataset:
- **Button:** "📥 Download Template CSV"
- **Button:** "📊 Download Template Excel"
- **Button:** "📂 Gunakan Data Sample"

### B. Interpretasi Threshold

| Metrik | Rendah (<33%) | Sedang (33-67%) | Tinggi (>67%) |
|--------|---------------|-----------------|---------------|
| IPM | < threshold_low | threshold_low - threshold_high | > threshold_high |
| Garis Kemiskinan | < threshold_low | threshold_low - threshold_high | > threshold_high |
| Pengeluaran | < threshold_low | threshold_low - threshold_high | > threshold_high |

**Note:** Threshold dihitung dari percentile data yang di-upload.

### C. Keyboard Shortcuts

- `Ctrl + U` atau `Cmd + U`: Fokus ke upload area
- `Enter`: Submit form (jika di input field)
- `Esc`: Close modals
- `Ctrl + S` atau `Cmd + S`: Download PDF (jika di hasil page)

---

**END OF MANUAL BOOK**

**Version:** 1.0  
**Last Updated:** October 2025  
**Total Pages:** 50+

---

*Untuk informasi lebih lanjut, lihat dokumentasi teknis di folder `/docs`*
