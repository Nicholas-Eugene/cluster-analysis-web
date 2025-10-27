# 🐛 Bug Fix: 500 Error on All Years Upload

## Problem

Saat mengupload file dengan mode "all_years", API mengembalikan error 500 (Internal Server Error).

**Error Message:**
```
500 Internal Server Error
Expected response
```

---

## Root Cause

Ditemukan **indentation error** di file `backend/clustering/views.py` yang terjadi saat refactoring untuk clean code.

### Kode Bermasalah:

```python
class UploadAndProcessView(APIView):
    def post(self, request):
        # Parameter parsing
        try:
            algorithm = request.POST.get("algorithm", ALGORITHM_FCM)
            # ... other parameters
        except Exception as e:
            return Response({"error": ...}, status=400)
    
    def _parse_selected_years(self, selected_years_json):
        # Helper method
        return None

        # ❌ BUG: Kode di bawah ini tidak ter-indent dengan benar!
        # Seharusnya masih bagian dari method post(), bukan setelah _parse_selected_years()
        
        # Read and validate file
        try:
            df = read_data_file(file_obj)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        
        # ... rest of the clustering logic
```

**Masalah:**
- Kode untuk membaca file dan menjalankan clustering tidak ter-indent dengan benar
- Kode tersebut berada di luar method `post()`, sehingga tidak pernah dieksekusi
- Method `post()` berakhir setelah parsing parameters, tanpa melakukan clustering
- Ini menyebabkan response tidak pernah dikembalikan, menghasilkan 500 error

---

## Solution

### Fix yang Dilakukan:

1. **Perbaiki Indentation di Method `post()`**
   - Pindahkan kode file reading dan clustering logic ke dalam method `post()`
   - Pastikan semua kode ter-indent dengan benar sebagai bagian dari method

2. **Pindahkan Helper Method ke Posisi yang Benar**
   - Pindahkan `_parse_selected_years()` ke posisi yang benar (setelah method `post()` selesai)

### Kode Setelah Fix:

```python
class UploadAndProcessView(APIView):
    def post(self, request):
        """Process uploaded file and perform clustering analysis."""
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"error": "File tidak ditemukan"}, status=400)

        # Parse and validate parameters
        try:
            algorithm = request.POST.get("algorithm", ALGORITHM_FCM).lower()
            num_clusters = safe_int_conversion(request.POST.get("num_clusters"), 3)
            # ... other parameters
            selected_years = self._parse_selected_years(request.POST.get("selected_years"))
        except Exception as e:
            return Response({"error": f"Parameter tidak valid: {str(e)}"}, status=400)

        # ✅ FIX: Kode ini sekarang ter-indent dengan benar sebagai bagian dari post()
        
        # Read and validate file
        try:
            df = read_data_file(file_obj)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        # Normalize column names
        df, column_mapping = normalize_column_names(df)
        
        # Validate required columns
        missing_cols = validate_required_columns(df)
        if missing_cols:
            return Response({"error": f'Kolom wajib hilang: {missing_cols}'}, status=400)

        # Clean and validate data
        try:
            df = clean_and_validate_data(df)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        # Format parameters
        parameters = format_clustering_parameters(...)

        # Validate algorithm
        if algorithm not in SUPPORTED_ALGORITHMS:
            return Response({"error": "Algoritma tidak dikenal"}, status=400)

        # Execute clustering
        try:
            results = self._execute_clustering(
                df=df,
                algorithm=algorithm,
                clustering_mode=clustering_mode,
                # ... other parameters
            )
            results["clustering_mode"] = clustering_mode
        except Exception as e:
            return Response({"error": f"Gagal melakukan clustering: {str(e)}"}, status=500)

        # Save session
        with transaction.atomic():
            session = ClusteringSession.objects.create(
                original_filename=getattr(file_obj, "name", ""),
                parameters=parameters,
                results=results,
            )

        return Response(
            {"session_id": str(session.id), "results": results},
            status=status.HTTP_201_CREATED,
        )
    
    # ✅ FIX: Helper methods sekarang di posisi yang benar (setelah post())
    
    def _parse_selected_years(self, selected_years_json):
        """Parse selected years from JSON string."""
        if not selected_years_json:
            return None
        
        try:
            selected_years = json.loads(selected_years_json)
            if selected_years:
                selected_years = [int(y) for y in selected_years]
                print(f"🎯 Selected years from request: {selected_years}")
                return selected_years
        except Exception as e:
            print(f"⚠️ Error parsing selected_years: {e}")
        
        return None
    
    def _execute_clustering(self, **params):
        """Execute clustering based on mode and algorithm."""
        # Implementation...
    
    def _run_all_years_clustering(self, **params):
        """Run clustering for all years combined."""
        # Implementation...
    
    def _run_per_year_clustering(self, **params):
        """Run clustering per year."""
        # Implementation...
```

---

## Files Changed

- `backend/clustering/views.py` - Fixed indentation and method ordering

---

## Testing

### Test Case 1: Upload dengan Mode "All Years"
```bash
# Request
POST /api/clustering/upload
Content-Type: multipart/form-data

{
    "file": <excel_file>,
    "algorithm": "fcm",
    "num_clusters": 3,
    "clustering_mode": "all_years"
}

# Expected Response (sebelum fix: 500 error)
# After fix: 201 Created
{
    "session_id": "uuid-here",
    "results": {
        "clustering_type": "all_years_wide",
        "overall_summary": {...},
        "results_per_year": {
            "all_years": {...}
        }
    }
}
```

### Test Case 2: Upload dengan Mode "Per Year"
```bash
# Request
POST /api/clustering/upload
Content-Type: multipart/form-data

{
    "file": <excel_file>,
    "algorithm": "fcm",
    "num_clusters": 3,
    "clustering_mode": "per_year"
}

# Expected Response: 201 Created (sudah bekerja sebelumnya)
{
    "session_id": "uuid-here",
    "results": {
        "clustering_type": "per_year",
        "overall_summary": {...},
        "results_per_year": {
            "2015": {...},
            "2016": {...},
            ...
        }
    }
}
```

---

## Verification

### Pre-Fix Status:
- ❌ All years mode: 500 Error
- ✅ Per year mode: Working

### Post-Fix Status:
- ✅ All years mode: Working
- ✅ Per year mode: Still working

### Linter Status:
```bash
No linter errors found.
```

---

## Lessons Learned

### 1. **Be Careful with Indentation in Python**
Python sangat sensitif terhadap indentation. Satu kesalahan indentation bisa menyebabkan logic tidak dieksekusi.

### 2. **Test After Refactoring**
Selalu test semua flow setelah refactoring, bahkan untuk perubahan yang terlihat sederhana.

### 3. **Use Linter, But Also Manual Review**
Linter tidak selalu menangkap logical errors seperti ini. Manual review tetap penting.

### 4. **Method Ordering Matters**
Pastikan helper methods ditempatkan di posisi yang benar dalam class.

---

## Prevention for Future

### 1. Add Unit Tests
```python
# tests/test_views.py
def test_upload_all_years_mode():
    """Test upload with all_years clustering mode."""
    response = client.post('/api/clustering/upload', data={
        'file': test_file,
        'clustering_mode': 'all_years',
        'algorithm': 'fcm',
    })
    assert response.status_code == 201
    assert 'session_id' in response.json()
```

### 2. Add Integration Tests
Test both clustering modes to ensure they work.

### 3. Use Code Review
Have someone review refactoring changes before deployment.

---

## Status

✅ **FIXED** - All years upload now works correctly

---

**Fixed by:** Clean Code Refactoring Team  
**Date:** 2025-10-20  
**Severity:** High (API completely broken for all_years mode)  
**Impact:** All users using all_years clustering mode  
