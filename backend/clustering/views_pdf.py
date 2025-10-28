from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from .pdf_generator import generate_cluster_report
import json


from django.http import HttpResponse
from wsgiref.util import FileWrapper
import mimetypes


class DownloadClusterReportView(APIView):
    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Accept"
        return response

    def post(self, request):
        """
        Generate and download a PDF report of clustering results
        """
        try:
            # Get clustering results from request body
            clustering_results = request.data.get("clustering_results")
            if not clustering_results:
                return Response(
                    {"error": "Hasil clustering tidak ditemukan"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Validate required fields
            if not isinstance(clustering_results, dict):
                return Response(
                    {"error": "Format data clustering tidak valid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if "yearly_results" not in clustering_results:
                return Response(
                    {"error": "Data hasil clustering per tahun tidak ditemukan"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Log the structure for debugging
            print("Received clustering results structure:")
            print(f"Keys in clustering_results: {clustering_results.keys()}")
            print("\nSample of yearly_results:")
            for year, data in clustering_results.get("yearly_results", {}).items():
                print(f"\nYear {year}:")
                print(f"Has data: {bool(data.get('data'))}")
                print(f"Number of data points: {len(data.get('data', []))}")
                print(f"Evaluation scores: {data.get('evaluation', {})}")
                print(f"Number of clusters: {len(data.get('clusters', []))}")
                break  # Just show first year as sample
            print(f"Years available: {clustering_results['yearly_results'].keys()}")

            for year, data in clustering_results["yearly_results"].items():
                print(f"\nYear {year} data structure:")
                print(f"Keys in year data: {data.keys()}")
                if "clusters" in data:
                    print(f"Number of clusters: {len(data['clusters'])}")

            # Generate PDF
            pdf_buffer = generate_cluster_report(clustering_results)

            # Create response
            response = HttpResponse(
                FileWrapper(pdf_buffer), content_type="application/pdf"
            )

            # Add headers
            response["Content-Disposition"] = (
                'attachment; filename="cluster_analysis_report.pdf"'
            )
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Expose-Headers"] = "Content-Disposition"

            return response

        except Exception as e:
            import traceback

            print("Error generating PDF:")
            print(traceback.format_exc())
            return Response(
                {"error": f"Error generating PDF: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
