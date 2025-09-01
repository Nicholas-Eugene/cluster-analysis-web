from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import ClusteringSession

import pandas as pd
import numpy as np


def compute_demo_fcm_results(df: pd.DataFrame, num_clusters: int) -> dict:
    # For initial implementation, return a shaped demo based on df
    clusters = []
    # naive split for demo
    df = df.copy()
    df['cluster'] = (np.arange(len(df)) % num_clusters)
    for cluster_id in range(num_clusters):
        members_df = df[df['cluster'] == cluster_id]
        centroid = {
            'ipm': float(members_df['ipm'].astype(float).mean()) if not members_df.empty else 0.0,
            'garis_kemiskinan': float(members_df['garis_kemiskinan'].astype(float).mean()) if not members_df.empty else 0.0,
        }
        members = []
        for _, row in members_df.iterrows():
            members.append({
                'kabupaten_kota': str(row.get('kabupaten_kota', '')),
                'tahun': int(row.get('tahun', 0)) if str(row.get('tahun', '')).isdigit() else row.get('tahun', 0),
                'ipm': float(row.get('ipm', 0.0)),
                'garis_kemiskinan': float(row.get('garis_kemiskinan', 0.0)),
                'membership': 1.0 / num_clusters,
            })
        clusters.append({'id': cluster_id, 'centroid': centroid, 'members': members})
    return {
        'summary': {
            'total_regions': int(df.shape[0]),
            'num_clusters': int(num_clusters),
            'iterations': 1,
            'execution_time': 0.01,
        },
        'evaluation': {
            'davies_bouldin': 0.0,
            'silhouette_score': 0.0,
        },
        'clusters': clusters,
    }


class UploadAndProcessView(APIView):
    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'File tidak ditemukan'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            num_clusters = int(request.POST.get('num_clusters', 3))
            fuzzy_coeff = float(request.POST.get('fuzzy_coeff', 2.0))
            max_iter = int(request.POST.get('max_iter', 300))
            tolerance = float(request.POST.get('tolerance', 0.0001))
            selected_year = request.POST.get('selected_year')
        except Exception:
            return Response({'error': 'Parameter tidak valid'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_csv(file_obj)
        except Exception:
            return Response({'error': 'Gagal membaca file CSV'}, status=status.HTTP_400_BAD_REQUEST)

        required_cols = {'kabupaten_kota', 'tahun', 'ipm', 'garis_kemiskinan'}
        if not required_cols.issubset(set(df.columns)):
            return Response({'error': 'Kolom wajib hilang: kabupaten_kota, tahun, ipm, garis_kemiskinan'}, status=status.HTTP_400_BAD_REQUEST)

        if selected_year:
            try:
                df = df[df['tahun'] == int(selected_year)]
            except Exception:
                pass

        parameters = {
            'num_clusters': num_clusters,
            'fuzzy_coeff': fuzzy_coeff,
            'max_iter': max_iter,
            'tolerance': tolerance,
            'selected_year': selected_year,
        }

        # TODO: replace with actual FCM; for now generate shaped results
        results = compute_demo_fcm_results(df, num_clusters)

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
