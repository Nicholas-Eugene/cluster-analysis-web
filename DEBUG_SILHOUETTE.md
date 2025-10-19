# 🔍 Debug Silhouette Score Issue

## ❓ Informasi Yang Dibutuhkan

Tolong berikan detail berikut:

### **1. Error Message Lengkap**
```
Contoh:
- "TypeError: ..."
- "ValueError: ..."
- "KeyError: ..."
- Screenshot error console
```

### **2. Lokasi Error**
- [ ] Frontend Console (Browser DevTools)
- [ ] Backend Terminal (Django server)
- [ ] Silhouette Plot tidak muncul
- [ ] Score menunjukkan NaN/undefined

### **3. Setup**
- Algoritma: FCM / OPTICS / Keduanya?
- Mode: Per Year / All Years?
- Tahun yang dipilih: ?

### **4. Behavior**
- [ ] Clustering berhasil tapi plot tidak muncul
- [ ] Error saat proses clustering
- [ ] Plot muncul tapi kosong
- [ ] Score menunjukkan nilai aneh

---

## 🔍 Kemungkinan Penyebab

### **Issue 1: Index Mismatch (FCM)**
```python
# Line 244-245 algorithms.py
if sil_samples is not None and idx < len(cluster_indices):
    member_info["silhouette_score"] = float(sil_samples[cluster_indices[idx]])
```

**Possible Problem:** 
- `idx` adalah enumerate index (cluster-specific)
- `cluster_indices[idx]` mapping ke full array index
- Bisa mismatch jika ada missing data

**Fix:**
```python
# Add boundary check
if sil_samples is not None and idx < len(cluster_indices) and cluster_indices[idx] < len(sil_samples):
    member_info["silhouette_score"] = float(sil_samples[cluster_indices[idx]])
```

---

### **Issue 2: NaN Values (OPTICS)**
```python
# Line 391-394 algorithms.py
if sil_samples is not None and idx < len(cluster_indices):
    sil_val = sil_samples[cluster_indices[idx]]
    if not np.isnan(sil_val):
        member_info["silhouette_score"] = float(sil_val)
```

**Possible Problem:**
- Noise points get NaN
- Some members might not have silhouette_score field

**Fix:** Already handled with `np.isnan` check

---

### **Issue 3: Frontend Fallback (SilhouettePlot.vue)**
```javascript
const getSilhouetteScore = (member) => {
  if (member.silhouette_score !== undefined && member.silhouette_score !== null) {
    return member.silhouette_score
  }
  return 0.5 // Fallback
}
```

**Possible Problem:**
- If many members missing score, plot looks weird
- Fallback to 0.5 might not be accurate

---

### **Issue 4: Empty Clusters**
**Problem:** If all clusters are filtered out (all noise)

**Fix:** Already handled in SilhouettePlot.vue:
```javascript
const validClusters = props.clusters.filter(c => c.id !== -1 && c.id !== '-1')
if (validClusters.length === 0) {
  console.log('❌ No valid clusters')
  return
}
```

---

## 🛠️ Quick Fixes

### **Fix 1: Add Boundary Check (FCM)**
```python
# backend/clustering/algorithms.py Line 244
if sil_samples is not None and idx < len(cluster_indices):
    global_idx = cluster_indices[idx]
    if global_idx < len(sil_samples):  # ADD THIS CHECK
        member_info["silhouette_score"] = float(sil_samples[global_idx])
```

### **Fix 2: Add Debug Logging**
```python
# After silhouette calculation
print(f"✅ Calculated silhouette samples: {len(sil_samples)} scores")
print(f"   Score range: [{np.min(sil_samples):.3f}, {np.max(sil_samples):.3f}]")
```

### **Fix 3: Frontend Safe Access**
```javascript
// SilhouettePlot.vue
const scores = cluster.members
  .map(member => ({
    score: getSilhouetteScore(member),
    name: member.kabupaten_kota || 'Unknown'
  }))
  .filter(item => !isNaN(item.score) && item.score !== null)  // ADD FILTER
```

---

## 🧪 Test Commands

### **Backend Test:**
```bash
cd /workspace/backend
python3 -c "
from clustering.algorithms import ClusteringEngine
import pandas as pd
import numpy as np

# Create test data
data = {
    'kabupaten_kota': ['A', 'B', 'C', 'D', 'E'],
    'provinsi': ['P1', 'P1', 'P2', 'P2', 'P3'],
    'tahun': [2020, 2020, 2020, 2020, 2020],
    'ipm': [70, 72, 68, 75, 71],
    'garis_kemiskinan': [800000, 850000, 780000, 900000, 820000],
    'pengeluaran_per_kapita': [12000, 13000, 11000, 15000, 12500],
    'latitude': [0.0, 0.0, 0.0, 0.0, 0.0],
    'longitude': [0.0, 0.0, 0.0, 0.0, 0.0]
}
df = pd.DataFrame(data)

engine = ClusteringEngine()
result = engine.fcm_clustering(
    df, 
    features=['ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita'],
    n_clusters=2
)

print('Clusters:', len(result['clusters']))
for cluster in result['clusters']:
    scores = [m.get('silhouette_score', 'N/A') for m in cluster['members']]
    print(f'Cluster {cluster[\"id\"]}: {len(scores)} members, scores: {scores}')
"
```

---

## 📝 Please Provide

**Copy-paste the following:**

1. **Full error message from browser console**
2. **Full error message from backend terminal** 
3. **Screenshot of the issue**
4. **Which algorithm + mode you're using**

Dengan informasi ini saya bisa fix dengan tepat! 🎯
