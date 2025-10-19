# 🤖 Logika Interpretasi Cluster - Menggunakan Data Normalisasi

## ✅ UPDATE: Logika Baru dengan Data Normalisasi

Backend sekarang menggunakan **data normalisasi** untuk **semua 3 variabel**:
1. ✅ IPM (normalized)
2. ✅ Pengeluaran Per Kapita (normalized)
3. ✅ Garis Kemiskinan (normalized)

---

## 🎯 Konsep Baru

### **Daerah Maju dengan Biaya Hidup Mahal:**

**Karakteristik:**
- ✅ IPM tinggi (> 67% dari range)
- ✅ Pengeluaran per kapita tinggi (> 67% dari range)
- ✅ Garis kemiskinan tinggi (> 67% dari range)

**Interpretasi:**
```
Label: "Daerah Maju Biaya Tinggi"
Bukan daerah miskin! Ini daerah maju seperti Jakarta/Surabaya
yang punya biaya hidup mahal tapi kesejahteraan tinggi.
```

**Contoh:**
```
IPM: 82.0 (tinggi)
Pengeluaran: 19,000 ribu/tahun = Rp 1,583,333/bulan (tinggi)
Garis Kemiskinan: Rp 950,000/bulan (tinggi)
→ Daerah urban maju dengan standar hidup tinggi
```

---

## 📊 Kategori Label Baru

### **1. Daerah Maju Biaya Tinggi** 🟣
```python
if IPM > 67% AND Pengeluaran > 67% AND Garis_Kemiskinan > 67%:
    label = "Daerah Maju Biaya Tinggi"
    category = "prosperous_high_cost"
    color = "#9333ea"  # Purple
```

**Contoh:** Jakarta, Surabaya, Bandung  
**Karakteristik:** Maju, tapi mahal

---

### **2. Daerah Sejahtera Efisien** 🟢
```python
if IPM > 67% AND Pengeluaran > 67% AND Garis_Kemiskinan < 33%:
    label = "Daerah Sejahtera Efisien"
    category = "prosperous"
    color = "#48bb78"  # Green
```

**Contoh:** Daerah sejahtera dengan biaya hidup terjangkau  
**Karakteristik:** Ideal - sejahtera & affordable

---

### **3. Daerah Tertinggal** 🔴
```python
if IPM < 33% AND Pengeluaran < 33% AND Garis_Kemiskinan < 33%:
    label = "Daerah Tertinggal"
    category = "poor"
    color = "#f56565"  # Red
```

**Contoh:** Daerah pedalaman, kepulauan terpencil  
**Karakteristik:** Perlu perhatian khusus

---

### **4. Daerah Rentan Biaya Tinggi** 🟠
```python
if IPM < 33% AND Garis_Kemiskinan > 67%:
    label = "Daerah Rentan Biaya Tinggi"
    category = "vulnerable"
    color = "#ed8936"  # Orange
```

**Contoh:** Daerah dengan SDM rendah tapi biaya hidup tinggi  
**Karakteristik:** Problematic - perlu intervensi komprehensif

---

### **5. Daerah Berkembang Biaya Tinggi** 🔵
```python
if IPM > 67% AND Pengeluaran >= 33% AND Garis_Kemiskinan > 67%:
    label = "Daerah Berkembang Biaya Tinggi"
    category = "developing"
    color = "#4299e1"  # Blue
```

**Karakteristik:** SDM baik, biaya tinggi, sedang berkembang

---

### **6. Daerah Biaya Tinggi** 💜
```python
if Pengeluaran > 67% AND Garis_Kemiskinan > 67%:
    label = "Daerah Biaya Tinggi"
    category = "high_cost"
    color = "#a855f7"  # Light Purple
```

**Karakteristik:** Fokus pada biaya hidup tinggi

---

### **7. Daerah Berkembang** 🔵
```python
if IPM > 67%:
    label = "Daerah Berkembang"
    category = "developing"
    color = "#4299e1"  # Blue
```

**Karakteristik:** SDM baik dengan potensi

---

### **8. Daerah Miskin** 🔴
```python
if IPM < 33% AND pengeluaran < garis_kemiskinan:
    label = "Daerah Miskin"
    category = "poor"
    color = "#f56565"  # Red
```

**Karakteristik:** Perlu program pengentasan kemiskinan

---

### **9. Daerah Menengah** 🟡
```python
else:  # Default fallback
    label = "Daerah Menengah"
    category = "middle"
    color = "#ecc94b"  # Yellow
```

**Karakteristik:** Kondisi sedang, bisa ditingkatkan

---

## 🔄 Decision Tree

```
                    START
                      │
         ┌────────────┴────────────┐
         │                         │
    IPM > 67%?              IPM < 33%?
         │                         │
    ┌────YES────┐            ┌─────YES─────┐
    │           │            │              │
Pengeluaran  Pengeluaran  Pengeluaran   Pengeluaran
  > 67%?      sedang       > 67%?         < GK?
    │           │            │              │
   YES         NO          YES             YES
    │           │            │              │
   GK          │           GK              │
  > 67%?       │          > 67%?           │
    │          │            │              │
┌───YES───┐  DAERAH     ┌──YES──┐      DAERAH
│         │  BERKEMBANG │       │      MISKIN
│        NO             │      NO
│         │            │        │
│      DAERAH      DAERAH    DAERAH
│   SEJAHTERA     RENTAN    BIAYA
│    EFISIEN      BIAYA     TINGGI
│                 TINGGI
│
DAERAH MAJU
BIAYA TINGGI
```

---

## 📊 Contoh Test Results

### **Test Case 1: Daerah Maju Biaya Tinggi**
```
Input:
  IPM: 82.0 (max dalam dataset)
  Pengeluaran: 19,000 ribu/tahun (max dalam dataset)
  Garis Kemiskinan: Rp 950,000/bulan (max dalam dataset)

Normalized:
  IPM: 1.0 (tertinggi → 100%)
  Pengeluaran: 1.0 (tertinggi → 100%)
  Garis Kemiskinan: 1.0 (tertinggi → 100%)

Output:
  ✅ Label: "Daerah Maju Biaya Tinggi"
  ✅ Category: "prosperous_high_cost"
  ✅ Color: Purple (#9333ea)
  ✅ Desc: "Daerah maju dengan standar hidup tinggi..."
```

### **Test Case 2: Daerah Tertinggal**
```
Input:
  IPM: 64.0 (min dalam dataset)
  Pengeluaran: 7,500 ribu/tahun (min dalam dataset)
  Garis Kemiskinan: Rp 750,000/bulan (min dalam dataset)

Normalized:
  IPM: 0.0 (terendah → 0%)
  Pengeluaran: 0.0 (terendah → 0%)
  Garis Kemiskinan: 0.0 (terendah → 0%)

Output:
  ✅ Label: "Daerah Tertinggal"
  ✅ Category: "poor"
  ✅ Color: Red (#f56565)
  ✅ Desc: "Daerah tertinggal dengan IPM rendah..."
```

### **Test Case 3: Daerah Menengah**
```
Input:
  IPM: 72.0
  Pengeluaran: 12,000 ribu/tahun
  Garis Kemiskinan: Rp 850,000/bulan

Normalized:
  IPM: 0.444 (sedang → 44%)
  Pengeluaran: 0.391 (sedang → 39%)
  Garis Kemiskinan: 0.5 (sedang → 50%)

Output:
  ✅ Label: "Daerah Menengah"
  ✅ Category: "middle"
  ✅ Color: Yellow (#ecc94b)
  ✅ Desc: "Daerah dalam kondisi menengah..."
```

---

## 🎨 Response JSON dengan Normalized Data

```json
{
  "clusters": [
    {
      "id": 0,
      "centroid": {
        "ipm": 82.0,
        "garis_kemiskinan": 950000,
        "pengeluaran_per_kapita": 19000
      },
      "size": 25,
      "interpretation": {
        "label": "Daerah Maju Biaya Tinggi",
        "category": "prosperous_high_cost",
        "description": "Daerah maju dengan IPM tinggi (82.00), pengeluaran per kapita tinggi (19000 ribu/tahun atau Rp 1,583,333/bulan), dan garis kemiskinan tinggi (Rp 950,000/bulan). Daerah ini memiliki standar hidup tinggi dengan biaya hidup yang mahal, karakteristik daerah urban maju seperti kota besar.",
        "color_code": "#9333ea",
        "metrics": {
          "ipm_level": "Tinggi",
          "ipm_normalized": 1.0,
          "expenditure_level": "Tinggi",
          "expenditure_normalized": 1.0,
          "poverty_line_level": "Tinggi",
          "poverty_line_normalized": 1.0,
          "poverty_status": "Jauh Di Atas Garis Kemiskinan",
          "ipm_score": 82.0,
          "poverty_line_ratio": 1.67,
          "expenditure_per_month": 1583333,
          "poverty_line": 950000
        }
      }
    }
  ]
}
```

---

## 🔑 Key Improvements

### **SEBELUMNYA:**
❌ Hanya compare pengeluaran vs garis kemiskinan (ratio)  
❌ Garis kemiskinan tinggi → dianggap miskin  
❌ Tidak akurat untuk daerah urban maju  

### **SEKARANG:**
✅ Normalisasi **semua 3 variabel**  
✅ Garis kemiskinan tinggi + IPM tinggi + pengeluaran tinggi → **Daerah Maju**  
✅ Akurat untuk berbagai tipe daerah (urban/rural)  
✅ Contextual interpretation  

---

## 📋 Files Changed

```
Backend:
  cluster_interpreter.py  (REWRITTEN) ✅
    - Add gk_normalized calculation
    - Add new decision tree
    - Add new categories
    - Add normalized metrics to response

Total: ~100 lines rewritten
```

---

## 🚀 Cara Menggunakan

### **1. Restart Backend:**
```bash
cd /workspace/backend
# Stop server (Ctrl+C)
python manage.py runserver
```

### **2. Test di Frontend:**
```bash
# 1. Upload data
# 2. Process clustering
# 3. Lihat hasil
```

### **3. Expected Labels:**

**Jika data punya daerah urban maju:**
```
✅ "Daerah Maju Biaya Tinggi" (bukan "Cluster Miskin")
   - IPM: Tinggi
   - Pengeluaran: Tinggi  
   - Garis Kemiskinan: Tinggi
```

**Jika data punya daerah tertinggal:**
```
✅ "Daerah Tertinggal"
   - IPM: Rendah
   - Pengeluaran: Rendah
   - Garis Kemiskinan: Rendah
```

---

## 🎯 Summary

### **Logika Baru:**

**Menggunakan normalisasi untuk fair comparison:**

| Variable | Range | Normalized | Interpretation |
|----------|-------|------------|----------------|
| IPM | 64-82 | 0.0-1.0 | 0-33%: Rendah, 33-67%: Sedang, 67-100%: Tinggi |
| Pengeluaran | 7500-19000 | 0.0-1.0 | 0-33%: Rendah, 33-67%: Sedang, 67-100%: Tinggi |
| Garis Kemiskinan | 750k-950k | 0.0-1.0 | 0-33%: Rendah, 33-67%: Sedang, 67-100%: Tinggi |

**Decision:** Berdasarkan kombinasi 3 normalized values

---

## 🔍 Kategori Lengkap

1. **Daerah Maju Biaya Tinggi** 🟣 - IPM↑ Pengeluaran↑ GK↑
2. **Daerah Sejahtera Efisien** 🟢 - IPM↑ Pengeluaran↑ GK↓
3. **Daerah Tertinggal** 🔴 - IPM↓ Pengeluaran↓ GK↓
4. **Daerah Rentan Biaya Tinggi** 🟠 - IPM↓ GK↑
5. **Daerah Berkembang Biaya Tinggi** 🔵 - IPM↑ GK↑
6. **Daerah Biaya Tinggi** 💜 - Pengeluaran↑ GK↑
7. **Daerah Berkembang** 🔵 - IPM↑
8. **Daerah Miskin** 🔴 - IPM↓ Pengeluaran < GK
9. **Daerah Menengah** 🟡 - Default

---

**Status:** ✅ **IMPLEMENTED & TESTED**

**Restart backend untuk apply!** 🚀
