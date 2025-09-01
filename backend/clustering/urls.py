from django.urls import path
from .views import UploadAndProcessView, GetResultsView


urlpatterns = [
    path('clustering/upload/', UploadAndProcessView.as_view(), name='upload-and-process'),
    path('clustering/results/<uuid:session_id>/', GetResultsView.as_view(), name='get-results'),
]

