from django.urls import path
from .views import (
    UploadAndProcessView, 
    GetResultsView,
    ExportResultsView,
    GenerateReportView,
    GetGeographicalDataView,
    GetClusterDetailsView,
    GetEvaluationMetricsView
)


urlpatterns = [
    path('clustering/upload/', UploadAndProcessView.as_view(), name='upload-and-process'),
    path('clustering/results/<uuid:session_id>/', GetResultsView.as_view(), name='get-results'),
    path('clustering/export/<uuid:session_id>/', ExportResultsView.as_view(), name='export-results'),
    path('clustering/report/<uuid:session_id>/', GenerateReportView.as_view(), name='generate-report'),
    path('clustering/geography/<uuid:session_id>/', GetGeographicalDataView.as_view(), name='get-geographical-data'),
    path('clustering/cluster/<uuid:session_id>/<int:cluster_id>/', GetClusterDetailsView.as_view(), name='get-cluster-details'),
    path('clustering/evaluation/<uuid:session_id>/', GetEvaluationMetricsView.as_view(), name='get-evaluation-metrics'),
]

