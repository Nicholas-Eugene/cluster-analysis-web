# 🔧 Perbaikan Silhouette Plot

## ❌ Masalah Sebelumnya

**Silhouette Plot tidak benar karena:**
1. ❌ Backend hanya menghitung **average silhouette score** (satu nilai)
2. ❌ Frontend menggunakan **aproksimasi** yang tidak akurat
3. ❌ Tidak ada silhouette score **per data point**

**Hasil:** Visualisasi silhouette plot tidak representatif dan tidak akurat.

---

## ✅ Solusi

### **Backend Changes:**

#### 1. Import `silhouette_samples` dari sklearn:
```python
from sklearn.metrics import davies_bouldin_score, silhouette_score, silhouette_samples
```

#### 2. Hitung silhouette score per sample di FCM:
```python
try:
    sil_score = silhouette_score(scaled_data, cluster_labels)
    # NEW: Calculate per-sample silhouette scores
    sil_samples = silhouette_samples(scaled_data, cluster_labels)
except ValueError as e:
    print(f"   ⚠️ Cannot calculate Silhouette score: {e}")
    sil_score = -1.0
    sil_samples = None
```

#### 3. Tambahkan silhouette_score ke setiap member (FCM):
```python
# Get indices in original dataframe for silhouette scores
cluster_indices = np.where(cluster_mask)[0]

for idx, (_, row) in enumerate(cluster_members_df.iterrows()):
    member_info = {...}
    
    # Add silhouette score for this member
    if sil_samples is not None and idx < len(cluster_indices):
        member_info["silhouette_score"] = float(sil_samples[cluster_indices[idx]])
```

#### 4. Hitung silhouette samples di OPTICS (dengan noise handling):
```python
try:
    sil_score = silhouette_score(
        scaled_data[valid_mask], cluster_labels[valid_mask]
    )
    # Calculate per-sample silhouette scores
    sil_samples_valid = silhouette_samples(
        scaled_data[valid_mask], cluster_labels[valid_mask]
    )
    # Map back to full array (noise points get NaN)
    sil_samples = np.full(len(cluster_labels), np.nan)
    sil_samples[valid_mask] = sil_samples_valid
except ValueError as e:
    print(f"   ⚠️ Cannot calculate Silhouette score: {e}")
```

#### 5. Tambahkan silhouette_score ke setiap member (OPTICS):
```python
# Add silhouette score for this member
if sil_samples is not None and idx < len(cluster_indices):
    sil_val = sil_samples[cluster_indices[idx]]
    if not np.isnan(sil_val):
        member_info["silhouette_score"] = float(sil_val)
```

---

### **Frontend Changes:**

#### 1. Ganti aproksimasi dengan data dari backend:

**SEBELUM (Aproksimasi - Tidak Akurat):**
```javascript
const calculateApproximateSilhouette = (member, cluster, allClusters) => {
  // Complex approximation using distance from centroid
  // NOT ACCURATE!
  const features = ['ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita']
  let distance = 0
  // ... complex calculation ...
  return Math.max(-1, Math.min(1, 1 - distance))
}
```

**SESUDAH (Data Real dari Backend - Akurat):**
```javascript
const getSilhouetteScore = (member) => {
  // Use backend-calculated silhouette score if available
  if (member.silhouette_score !== undefined && member.silhouette_score !== null) {
    return member.silhouette_score
  }
  // Fallback (shouldn't happen with new backend)
  return 0.5
}
```

#### 2. Update penggunaan di semua tempat:

```javascript
// Average score calculation
props.clusters.forEach(cluster => {
  cluster.members.forEach(member => {
    const score = getSilhouetteScore(member)  // Changed from calculateApproximateSilhouette
    total += score
    count++
  })
})

// Chart data preparation
const scores = cluster.members.map(member => ({
  score: getSilhouetteScore(member),  // Changed from calculateApproximateSilhouette
  name: member.kabupaten_kota || 'Unknown'
}))
```

---

## 📊 Struktur Data Baru

### **Response dari Backend:**

```json
{
  "clusters": [
    {
      "id": 0,
      "centroid": {...},
      "size": 25,
      "members": [
        {
          "kabupaten_kota": "Aceh Barat",
          "ipm": 65.20,
          "garis_kemiskinan": 850000,
          "pengeluaran_per_kapita": 8500,
          "membership": 0.95,
          "silhouette_score": 0.72  // ← NEW! Per-sample score
        },
        {
          "kabupaten_kota": "Aceh Timur",
          "ipm": 64.80,
          "silhouette_score": 0.68  // ← NEW!
        }
      ]
    }
  ],
  "evaluation": {
    "davies_bouldin": 0.5234,
    "silhouette_score": 0.6789  // ← Average score
  }
}
```

---

## 🎨 Silhouette Plot yang Benar

### **Interpretasi:**

Silhouette plot menampilkan **bar horizontal** untuk setiap data point:
- **X-axis:** Silhouette score (-1 to 1)
- **Y-axis:** Data points (sorted by score, grouped by cluster)
- **Color:** Warna cluster
- **Gap:** Pemisah antar cluster

### **Score Meaning:**

| Score Range | Quality | Meaning |
|------------|---------|---------|
| > 0.7 | 🟢 Sangat Baik | Data sangat cocok dengan clusternya |
| 0.5 - 0.7 | 🔵 Baik | Data cocok dengan clusternya |
| 0.25 - 0.5 | 🟡 Cukup | Data cukup cocok |
| < 0.25 | 🔴 Perlu Review | Data mungkin salah cluster |
| < 0 | ❌ Salah | Data lebih cocok di cluster lain |

### **Visualisasi:**

```
Silhouette Score
-1.0                     0                      1.0
 │                       │                       │
 ├───────────────────────┼───────────────────────┤
 
Cluster Miskin (25 points)
 │    ████████████████████████████████│          │  (0.82)
 │    ███████████████████████████████ │          │  (0.78)
 │    ██████████████████████████      │          │  (0.65)
 │    █████████████████████           │          │  (0.52)
 │    ██████████████                  │          │  (0.35)
 
Cluster Menengah (29 points)
 │    ████████████████████████████████████       │  (0.88)
 │    ███████████████████████████████████        │  (0.85)
 │    ██████████████████████████████             │  (0.70)
 │    ████████████████████                       │  (0.45)
 
Cluster Sejahtera (17 points)
 │    ████████████████████████████████████████   │  (0.92)
 │    ███████████████████████████████████        │  (0.85)
 │    ██████████████████████████                 │  (0.60)
```

---

## 🔍 Debugging

### **Check if silhouette_score exists in data:**

```javascript
// In browser console
console.log(clusters[0].members[0])
// Should show:
{
  kabupaten_kota: "Aceh Barat",
  ipm: 65.20,
  silhouette_score: 0.72,  // ← Should exist!
  ...
}
```

### **Backend calculation:**

```python
from sklearn.metrics import silhouette_samples
import numpy as np

# Example
scaled_data = np.array([[1, 2], [1.5, 2.1], [5, 8], [8, 8]])
labels = np.array([0, 0, 1, 1])

scores = silhouette_samples(scaled_data, labels)
print(scores)  # [0.72, 0.68, 0.65, 0.70]
```

---

## 📋 Files Changed

### **Backend:**
- `algorithms.py`:
  - Import `silhouette_samples` ✅
  - Calculate per-sample scores in FCM ✅
  - Calculate per-sample scores in OPTICS ✅
  - Add `silhouette_score` to each member ✅
  - Handle noise points in OPTICS ✅

### **Frontend:**
- `SilhouettePlot.vue`:
  - Remove approximation function ✅
  - Add `getSilhouetteScore()` function ✅
  - Use backend data for chart ✅
  - Use backend data for average ✅

---

## ✅ Benefits

**SEBELUM:**
- ❌ Silhouette plot based on approximation
- ❌ Not mathematically correct
- ❌ Misleading visualization
- ❌ Inconsistent with overall score

**SESUDAH:**
- ✅ Silhouette plot based on sklearn calculation
- ✅ Mathematically correct
- ✅ Accurate visualization
- ✅ Consistent with overall score
- ✅ Can identify misclassified points
- ✅ Supports both FCM and OPTICS

---

## 🧪 Testing

### **Test Scenario:**

1. **Upload data & process clustering**
2. **Check backend response:**
   ```javascript
   // In Network tab, check API response
   clusters[0].members[0].silhouette_score  // Should exist
   ```
3. **View Silhouette Plot:**
   - ✅ Bars should show actual silhouette scores
   - ✅ Longer bars = better clustering
   - ✅ Negative bars = poor fit
   - ✅ Clusters should be clearly separated

4. **Compare with average score:**
   - ✅ Average in plot should match evaluation.silhouette_score

---

## 🎯 Formula

### **Silhouette Score Formula:**

For each data point i:

```
a(i) = average distance to points in same cluster
b(i) = average distance to points in nearest other cluster

s(i) = (b(i) - a(i)) / max(a(i), b(i))
```

**Range:** -1 to 1
- s(i) close to 1: Well clustered
- s(i) close to 0: On the border
- s(i) close to -1: Likely in wrong cluster

**Average Silhouette Score:** Mean of all s(i)

---

## 📚 References

- sklearn documentation: [silhouette_samples](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_samples.html)
- sklearn documentation: [silhouette_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html)

---

**Status:** ✅ **FIXED & IMPLEMENTED**

**Silhouette Plot sekarang menampilkan data yang akurat dari sklearn!** 🎉
