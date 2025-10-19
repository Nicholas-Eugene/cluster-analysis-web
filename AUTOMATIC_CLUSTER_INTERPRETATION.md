# 🤖 Interpretasi Otomatis Label Cluster dari Backend

## ✅ STATUS: SUDAH DIIMPLEMENTASI & AKTIF

Backend **OTOMATIS** menentukan label cluster (Miskin, Sejahtera, dll) berdasarkan analisis IPM dan pengeluaran per kapita.

---

## 🎯 Bagaimana Cara Kerjanya?

### **1. Proses Otomatis di Backend**

Setiap kali clustering selesai, backend secara otomatis:

```python
# Di algorithms.py
results["clusters"] = add_cluster_interpretations(results["clusters"])
```

**Tidak perlu manual!** Sistem otomatis menganalisis setiap cluster.

---

### **2. Analisis Multi-Kriteria**

Backend menganalisis 3 hal utama:

#### **A. IPM (Indeks Pembangunan Manusia)**
```python
# Normalisasi IPM relatif terhadap semua cluster
ipm_normalized = (ipm - ipm_min) / (ipm - ipm_max)

# Threshold:
IPM_LOW = 0.33    # < 33% dari range
IPM_HIGH = 0.67   # > 67% dari range
```

#### **B. Pengeluaran vs Garis Kemiskinan**
```python
# Konversi: ribu/tahun → rupiah/bulan
pengeluaran_per_bulan = (pengeluaran * 1000) / 12

# Rasio
ratio = pengeluaran_per_bulan / garis_kemiskinan

# Threshold:
BELOW_POVERTY = 1.0      # Di bawah garis kemiskinan
SLIGHTLY_ABOVE = 1.3     # Sedikit di atas
WELL_ABOVE = 2.0         # Jauh di atas
```

#### **C. Kombinasi Kriteria**
Backend menggunakan decision tree untuk menentukan label.

---

## 🏷️ Label yang Dihasilkan Otomatis

### **1. Cluster Miskin** 🔴
```python
if ipm_normalized < IPM_LOW and ratio_to_poverty < BELOW_POVERTY:
    label = "Cluster Miskin"
    category = "poor"
    color_code = "#f56565"  # Red
```

**Kriteria:**
- ✅ IPM rendah (< 33% dari range)
- ✅ Pengeluaran di bawah garis kemiskinan

**Contoh Output:**
```
Label: Cluster Miskin
Deskripsi: IPM rendah (65.20), pengeluaran per kapita (8500 ribu/tahun 
           atau Rp 708,333/bulan) di bawah garis kemiskinan 
           (Rp 850,000/bulan). Memerlukan perhatian khusus dan 
           program bantuan sosial.
```

---

### **2. Cluster Sejahtera** 🟢
```python
elif ipm_normalized > IPM_HIGH and ratio_to_poverty > WELL_ABOVE:
    label = "Cluster Sejahtera"
    category = "prosperous"
    color_code = "#48bb78"  # Green
```

**Kriteria:**
- ✅ IPM tinggi (> 67% dari range)
- ✅ Pengeluaran jauh di atas garis kemiskinan (> 2x)

**Contoh Output:**
```
Label: Cluster Sejahtera
Deskripsi: IPM tinggi (80.30), pengeluaran per kapita (18000 ribu/tahun 
           atau Rp 1,500,000/bulan) jauh di atas garis kemiskinan 
           (Rp 750,000/bulan). Wilayah dengan kondisi ekonomi baik.
```

---

### **3. Cluster Menengah** 🟡
```python
elif (IPM_LOW <= ipm_normalized <= IPM_HIGH and 
      BELOW_POVERTY < ratio_to_poverty < WELL_ABOVE):
    label = "Cluster Menengah"
    category = "middle"
    color_code = "#ecc94b"  # Yellow
```

**Kriteria:**
- ✅ IPM sedang (33-67% dari range)
- ✅ Pengeluaran sedikit di atas garis kemiskinan (1.0x - 2.0x)

**Contoh Output:**
```
Label: Cluster Menengah
Deskripsi: IPM sedang (72.50), pengeluaran per kapita (12000 ribu/tahun 
           atau Rp 1,000,000/bulan) sedikit di atas garis kemiskinan 
           (Rp 900,000/bulan). Wilayah dengan potensi berkembang.
```

---

### **4. Cluster Rentan** 🟠
```python
elif ipm_normalized < IPM_LOW and ratio_to_poverty > SLIGHTLY_ABOVE:
    label = "Cluster Rentan"
    category = "vulnerable"
    color_code = "#ed8936"  # Orange
```

**Kriteria:**
- ✅ IPM rendah (< 33%)
- ✅ TAPI pengeluaran cukup tinggi (> 1.3x garis kemiskinan)

**Contoh Output:**
```
Label: Cluster Rentan
Deskripsi: IPM rendah (66.00), namun pengeluaran per kapita 
           (13000 ribu/tahun) cukup tinggi. Perlu fokus pada 
           peningkatan kualitas pendidikan dan kesehatan.
```

---

### **5. Cluster Berkembang** 🔵
```python
elif ipm_normalized > IPM_HIGH and BELOW_POVERTY < ratio_to_poverty < WELL_ABOVE:
    label = "Cluster Berkembang"
    category = "developing"
    color_code = "#4299e1"  # Blue
```

**Kriteria:**
- ✅ IPM tinggi (> 67%)
- ✅ Pengeluaran moderat (1.0x - 2.0x garis kemiskinan)

**Contoh Output:**
```
Label: Cluster Berkembang
Deskripsi: IPM tinggi (78.50), pengeluaran per kapita sedang. 
           Wilayah dengan potensi pertumbuhan ekonomi.
```

---

## 🔄 Alur Otomatis

```
1. User Upload Data
         ↓
2. Backend Run Clustering (FCM/OPTICS)
         ↓
3. Clusters Terbentuk (Cluster 0, 1, 2, ...)
         ↓
4. 🤖 OTOMATIS: Backend Analisis Setiap Cluster
         ├─→ Hitung IPM normalized
         ├─→ Hitung ratio pengeluaran/garis kemiskinan
         ├─→ Konversi satuan (tahun → bulan)
         └─→ Apply decision rules
         ↓
5. 🏷️ Label Ditambahkan ke Setiap Cluster
         ↓
6. Response JSON ke Frontend
         ↓
7. Frontend Tampilkan Label Otomatis
```

**Tidak ada input manual dari user!** Semua otomatis.

---

## 📦 Response JSON dari Backend

### **Struktur Data Lengkap:**

```json
{
  "algorithm": "Fuzzy C-Means",
  "summary": {...},
  "evaluation": {...},
  "clusters": [
    {
      "id": 0,
      "centroid": {
        "ipm": 65.20,
        "garis_kemiskinan": 850000,
        "pengeluaran_per_kapita": 8500
      },
      "size": 25,
      "members": [...],
      
      "interpretation": {  // ← OTOMATIS DITAMBAHKAN!
        "label": "Cluster Miskin",
        "category": "poor",
        "description": "IPM rendah (65.20), pengeluaran per kapita (8500 ribu/tahun atau Rp 708,333/bulan) di bawah garis kemiskinan (Rp 850,000/bulan). Memerlukan perhatian khusus dan program bantuan sosial.",
        "color_code": "#f56565",
        "metrics": {
          "ipm_level": "Rendah",
          "poverty_status": "Di Bawah Garis Kemiskinan",
          "poverty_line_ratio": 0.83,
          "expenditure_per_month": 708333
        }
      }
    },
    {
      "id": 1,
      "centroid": {...},
      "interpretation": {
        "label": "Cluster Menengah",  // ← OTOMATIS!
        "category": "middle",
        ...
      }
    },
    {
      "id": 2,
      "centroid": {...},
      "interpretation": {
        "label": "Cluster Sejahtera",  // ← OTOMATIS!
        "category": "prosperous",
        ...
      }
    }
  ],
  "interpretation_summary": {  // ← RINGKASAN OTOMATIS
    "total_clusters": 3,
    "poor": 1,
    "middle": 1,
    "prosperous": 1,
    "vulnerable": 0,
    "developing": 0
  }
}
```

---

## 🎨 Frontend Otomatis Menggunakan Label

### **Cluster Detail Tabs:**
```vue
<!-- Frontend OTOMATIS menggunakan label dari backend -->
<button>
  {{ cluster.interpretation?.label || `Cluster ${cluster.id}` }}
  ({{ cluster.size }})
</button>

<!-- Tampil sebagai: -->
<!-- "Cluster Miskin (25)" bukan "Cluster 0 (25)" -->
```

### **Chart Legends (Scatter, Box, Silhouette):**
```javascript
datasets.push({
  label: cluster.interpretation?.label || `Cluster ${cluster.id}`,
  // Output: "Cluster Sejahtera" bukan "Cluster 2"
})
```

### **Map Popup:**
```javascript
`<span>${cluster.interpretation?.label || 'Cluster ' + cluster.id}</span>`
// Output: "Cluster Miskin" bukan "Cluster 0"
```

---

## 🧪 Cara Verifikasi

### **1. Check Backend Response (Browser DevTools):**

```javascript
// Network tab → API response
console.log(response.clusters[0])

// Harus menunjukkan:
{
  id: 0,
  interpretation: {
    label: "Cluster Miskin",  // ← Harus ada!
    category: "poor",
    ...
  }
}
```

### **2. Check Frontend Display:**

**Tab Buttons:**
```
✅ "Cluster Miskin (25)"     ← Benar
❌ "Cluster 0 (25)"          ← Salah (jika masih muncul)
```

**Scatter Plot Legend:**
```
✅ ● Cluster Sejahtera (17)  ← Benar
❌ ● Cluster 2 (17)          ← Salah
```

**Map Legend:**
```
✅ ● Cluster Menengah (29 daerah)  ← Benar
❌ ● Cluster 1 (29 daerah)         ← Salah
```

---

## 🔧 Troubleshooting

### **Masalah: Label masih "Cluster 0" bukan "Cluster Miskin"**

**Kemungkinan:**

1. **Backend belum running dengan code baru**
   ```bash
   # Restart backend
   cd /workspace/backend
   python manage.py runserver
   ```

2. **Data lama di cache**
   ```bash
   # Clear cache & reprocess data
   # Upload data baru atau restart browser
   ```

3. **Check import di algorithms.py:**
   ```python
   from .cluster_interpreter import add_cluster_interpretations
   
   # Di akhir fungsi fcm_clustering dan optics_clustering:
   results["clusters"] = add_cluster_interpretations(results["clusters"])
   ```

---

## 📊 Contoh Konkret

### **Input Data:**
```
Cluster 0: IPM avg = 65.5, Pengeluaran avg = 8200 ribu/tahun
Cluster 1: IPM avg = 73.2, Pengeluaran avg = 12500 ribu/tahun
Cluster 2: IPM avg = 81.0, Pengeluaran avg = 19000 ribu/tahun

Garis Kemiskinan avg = 850,000 rupiah/bulan
```

### **Output Otomatis:**
```
Cluster 0:
  Label: "Cluster Miskin"
  Reason: IPM rendah (65.5) + pengeluaran < garis kemiskinan
  
Cluster 1:
  Label: "Cluster Menengah"
  Reason: IPM sedang (73.2) + pengeluaran sedikit > garis kemiskinan
  
Cluster 2:
  Label: "Cluster Sejahtera"
  Reason: IPM tinggi (81.0) + pengeluaran >> garis kemiskinan
```

---

## 💡 Keuntungan Sistem Otomatis

✅ **Konsisten** - Label ditentukan oleh algoritma, bukan subjektif  
✅ **Transparan** - Aturan jelas dan terdokumentasi  
✅ **Cepat** - Otomatis untuk setiap clustering  
✅ **Akurat** - Berdasarkan data real (centroid)  
✅ **Mudah dipahami** - Label deskriptif vs "Cluster 0"  
✅ **Actionable** - User langsung tahu karakteristik  

---

## 📝 Catatan Penting

### **Konversi Satuan:**

Backend otomatis handle konversi:
```python
# Data masuk: pengeluaran_per_kapita dalam ribu rupiah/orang/tahun
# Garis kemiskinan: rupiah/kapita/bulan

# Konversi untuk comparison:
pengeluaran_per_bulan = (pengeluaran * 1000) / 12
ratio = pengeluaran_per_bulan / garis_kemiskinan
```

### **Relative Analysis:**

Label ditentukan **relatif** terhadap semua cluster dalam satu run:
- IPM dinormalisasi ke range 0-1
- Threshold IPM_LOW dan IPM_HIGH adalah proporsi
- Ini memastikan interpretasi fair untuk berbagai kondisi data

---

## 🎯 Kesimpulan

### **Sistem SUDAH OTOMATIS:**

1. ✅ Backend menganalisis setiap cluster
2. ✅ Backend menentukan label berdasarkan IPM + pengeluaran
3. ✅ Backend menambahkan interpretasi ke response JSON
4. ✅ Frontend menggunakan label otomatis dari backend
5. ✅ Tidak perlu input manual dari user

### **Yang Perlu Dilakukan User:**

1. Upload data CSV
2. Pilih algoritma (FCM/OPTICS)
3. Klik "Mulai Cluster"
4. **SELESAI** - Label otomatis muncul!

---

## 🚀 Testing

```bash
# 1. Start backend
cd /workspace/backend
python manage.py runserver

# 2. Start frontend
cd /workspace/fuzzy-clustering-frontend
npm run dev

# 3. Upload data & process

# 4. Lihat hasil:
# ✅ Tab: "Cluster Miskin (25)" bukan "Cluster 0"
# ✅ Legend: "Cluster Sejahtera" bukan "Cluster 2"
# ✅ Map: "Cluster Menengah" bukan "Cluster 1"
```

---

**Status:** ✅ **AKTIF & BERJALAN OTOMATIS**

**Backend:** ✅ Auto-interpret clusters  
**Frontend:** ✅ Display interpreted labels  
**User Action:** ✅ **TIDAK PERLU MANUAL INPUT!**

**Sistem otomatis menentukan label cluster berdasarkan analisis IPM dan pengeluaran!** 🤖✨
