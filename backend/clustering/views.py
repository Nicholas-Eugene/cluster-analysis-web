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
            df = pd.read_csv(file_obj)
        except Exception as e:
            return Response({'error': f'Gagal membaca file CSV: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        required_cols = {'kabupaten_kota', 'tahun', 'ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita'}
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            return Response({'error': f'Kolom wajib hilang: {", ".join(missing_cols)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter by year if specified
        if selected_year:
            try:
                year_int = int(selected_year)
                df = df[df['tahun'] == year_int]
                if df.empty:
                    return Response({'error': f'Tidak ada data untuk tahun {selected_year}'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                pass

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
                    error=tolerance
                )
            elif algorithm == 'optics':
                results = get_clustering_results(
                    df,
                    algorithm='optics',
                    features=['ipm', 'garis_kemiskinan', 'pengeluaran_per_kapita'],
                    min_samples=min_samples,
                    xi=xi,
                    min_cluster_size=min_cluster_size
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
