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

        # Check for required columns - either long format or wide format
        has_kabupaten_col = 'kabupaten/kota' in df.columns or 'kabupaten_kota' in df.columns
        
        if not has_kabupaten_col:
            return Response({'error': 'Kolom "kabupaten/kota" atau "kabupaten_kota" diperlukan'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if it's wide format (has year columns) or long format
        has_year_columns = any('_' in col and col.split('_')[-1].isdigit() for col in df.columns)
        
        if has_year_columns:
            # Wide format - check for year-specific columns
            years_found = set()
            for col in df.columns:
                if '_' in col:
                    try:
                        year = int(col.split('_')[-1])
                        if 2015 <= year <= 2025:
                            years_found.add(year)
                    except ValueError:
                        continue
            
            if not years_found:
                return Response({'error': 'Tidak ditemukan kolom tahun yang valid (format: ipm_2016, pengeluaran_2016, dll.)'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if we have the required metric columns for at least one year
            required_metrics = ['ipm', 'pengeluaran', 'garis_kemiskinan']
            has_complete_year = False
            
            for year in years_found:
                year_cols = [f'{metric}_{year}' for metric in required_metrics]
                if all(col in df.columns for col in year_cols):
                    has_complete_year = True
                    break
            
            if not has_complete_year:
                return Response({'error': 'Tidak ditemukan tahun dengan data lengkap (ipm, pengeluaran, garis_kemiskinan)'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            # Long format - check for required columns
            required_cols = {'tahun', 'ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita'}
            missing_cols = required_cols - set(df.columns)
            if missing_cols:
                return Response({'error': f'Kolom wajib hilang: {", ".join(missing_cols)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Note: Year filtering will be handled in the clustering algorithms
        # for wide format data, as it needs to be converted to long format first

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
            # Use the new clustering algorithms
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
