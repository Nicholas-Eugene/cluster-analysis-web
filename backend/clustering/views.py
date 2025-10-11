from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import ClusteringSession
from .algorithms import get_clustering_results

import pandas as pd
import numpy as np


class UploadAndProcessView(APIView):
    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'File tidak ditemukan'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            algorithm = request.POST.get('algorithm', 'fcm').lower()
            num_clusters = int(request.POST.get('num_clusters', 3))
            fuzzy_coeff = float(request.POST.get('fuzzy_coeff', 2.0))
            max_iter = int(request.POST.get('max_iter', 300))
            tolerance = float(request.POST.get('tolerance', 0.0001))
            selected_year = request.POST.get('selected_year')
            
            # OPTICS specific parameters
            min_samples = int(request.POST.get('min_samples', 5))
            xi = float(request.POST.get('xi', 0.05))
            min_cluster_size = float(request.POST.get('min_cluster_size', 0.05))
        except Exception as e:
            return Response({'error': f'Parameter tidak valid: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Detect file type and read accordingly
            filename = getattr(file_obj, 'name', '').lower()
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                df = pd.read_excel(file_obj, engine='openpyxl')
            elif filename.endswith('.csv'):
                df = pd.read_csv(file_obj)
            else:
                # Try CSV first, then Excel
                try:
                    df = pd.read_csv(file_obj)
                except:
                    file_obj.seek(0)  # Reset file pointer
                    df = pd.read_excel(file_obj, engine='openpyxl')
        except Exception as e:
            return Response({'error': f'Gagal membaca file: {str(e)}. Pastikan file dalam format CSV atau Excel (.xlsx)'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for required columns - long format only (5 columns)
        # Normalize column names for flexible matching
        df_columns_lower = [col.lower().replace('/', '_').replace(' ', '_') for col in df.columns]
        df_columns_map = {col.lower().replace('/', '_').replace(' ', '_'): col for col in df.columns}
        
        required_cols = {
            'kabupaten_kota': ['kabupaten_kota', 'kabupaten/kota', 'kabupaten kota'],
            'tahun': ['tahun'],
            'ipm': ['ipm'],
            'garis_kemiskinan': ['garis_kemiskinan', 'garis kemiskinan'],
            'pengeluaran_per_kapita': ['pengeluaran_per_kapita', 'pengeluaran per kapita', 'pengeluaran_perkapita']
        }
        
        missing_cols = []
        column_mapping = {}
        
        for required_col, possible_names in required_cols.items():
            found = False
            for possible_name in possible_names:
                normalized_name = possible_name.lower().replace('/', '_').replace(' ', '_')
                if normalized_name in df_columns_lower:
                    # Map the required column to the actual column name in the dataframe
                    actual_col_name = df_columns_map[normalized_name]
                    column_mapping[required_col] = actual_col_name
                    found = True
                    break
            
            if not found:
                missing_cols.append(required_col)
        
        if missing_cols:
            return Response({'error': f'Kolom wajib hilang: {", ".join(missing_cols)}'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Rename columns to standardized names for consistent processing
        df = df.rename(columns={v: k for k, v in column_mapping.items()})

        # Validate data types and clean data
        try:
            # Ensure tahun is numeric
            df['tahun'] = pd.to_numeric(df['tahun'], errors='coerce')
            
            # Ensure numeric columns are numeric
            df['ipm'] = pd.to_numeric(df['ipm'], errors='coerce')
            df['garis_kemiskinan'] = pd.to_numeric(df['garis_kemiskinan'], errors='coerce')
            df['pengeluaran_per_kapita'] = pd.to_numeric(df['pengeluaran_per_kapita'], errors='coerce')
            
            # Remove rows with invalid data
            df = df.dropna(subset=['tahun', 'ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita'])
            
            if df.empty:
                return Response({'error': 'Tidak ada data valid yang dapat diproses. Pastikan semua kolom numerik berisi angka yang valid.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Ensure kabupaten_kota is string and not empty
            df['kabupaten_kota'] = df['kabupaten_kota'].astype(str).str.strip()
            df = df[df['kabupaten_kota'] != '']
            
            if df.empty:
                return Response({'error': 'Tidak ada data valid yang dapat diproses. Pastikan kolom kabupaten_kota tidak kosong.'}, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({'error': f'Error dalam validasi data: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Data is now in standardized long format with consistent column names and validated data types

        parameters = {
            'algorithm': algorithm,
            'num_clusters': num_clusters,
            'fuzzy_coeff': fuzzy_coeff,
            'max_iter': max_iter,
            'tolerance': tolerance,
            'selected_year': selected_year,
            'min_samples': min_samples,
            'xi': xi,
            'min_cluster_size': min_cluster_size,
        }

        try:
            # Determine clustering mode based on selected_year
            if selected_year:
                # Single year clustering
                clustering_mode = 'single_year'
                print(f"🎯 Single year clustering for {selected_year}")
            else:
                # Per year clustering (default new behavior)
                clustering_mode = 'per_year'
                print(f"🗓️ Per year clustering for all available years")
            
            # Use the clustering algorithms
            if algorithm == 'fcm':
                results = get_clustering_results(
                    df, 
                    algorithm='fcm',
                    features=['ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita'],
                    n_clusters=num_clusters,
                    m=fuzzy_coeff,
                    max_iter=max_iter,
                    error=tolerance,
                    selected_year=selected_year
                )
            elif algorithm == 'optics':
                results = get_clustering_results(
                    df,
                    algorithm='optics',
                    features=['ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita'],
                    min_samples=min_samples,
                    xi=xi,
                    min_cluster_size=min_cluster_size,
                    selected_year=selected_year
                )
            else:
                return Response({'error': 'Algoritma tidak dikenal. Gunakan "fcm" atau "optics"'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Add clustering mode to results
            results['clustering_mode'] = clustering_mode
                
        except Exception as e:
            return Response({'error': f'Gagal melakukan clustering: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        with transaction.atomic():
            session = ClusteringSession.objects.create(
                original_filename=getattr(file_obj, 'name', ''),
                parameters=parameters,
                results=results,
            )

        return Response({'session_id': str(session.id), 'results': results}, status=status.HTTP_201_CREATED)


class GetResultsView(APIView):
    def get(self, request, session_id: str):
        try:
            session = ClusteringSession.objects.get(id=session_id)
        except ClusteringSession.DoesNotExist:
            return Response({'error': 'Session tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
        return Response(session.results, status=status.HTTP_200_OK)
