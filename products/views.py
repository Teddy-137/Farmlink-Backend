from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import requests
from rest_framework import filters

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "category", "producer__username"]
    ordering_fields = ["price", "quality_grade"]

    def get_permissions(self):
        if self.action in ["destroy", "update", "partial_update"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated or self.request.user.role != 'producer':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only producers can create products.')
        serializer.save(producer=self.request.user)


# Placeholder for AI endpoints (to be implemented)


class QualityGradingAPIView(APIView):
    def post(self, request):
        product_type = request.data.get("product_type")
        criteria = request.data.get("criteria")
        photo = request.FILES.get("photo")
        if not (product_type and criteria and photo):
            return Response(
                {"error": "Missing required fields."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Save photo temporarily
        from django.core.files.storage import default_storage

        temp_path = default_storage.save(photo.name, photo)
        photo_path = default_storage.path(temp_path)
        # Prepare Gemini API call
        api_key = os.environ.get("GEMINI_API_KEY")
        with open(photo_path, "rb") as img_file:
            image_data = img_file.read()
        prompt = f"Analyze the provided image of {product_type} and grade its quality based on the following criteria: {criteria}. Provide a quality score from 1 to 10 and a brief explanation."
        # Example Gemini API call (pseudo, replace with real endpoint)
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
            params={"key": api_key},
            json={
                "contents": [
                    {
                        "parts": [
                            {"text": prompt},
                            {
                                "inline_data": {
                                    "mime_type": photo.content_type,
                                    "data": image_data.decode("latin1"),
                                }
                            },
                        ]
                    }
                ]
            },
        )
        if response.status_code == 200:
            result = response.json()
            # Parse result for score and explanation (pseudo)
            return Response({"result": result}, status=200)
        return Response({"error": "AI service failed."}, status=500)


class MarketAnalysisAPIView(APIView):
    def post(self, request):
        data_points = request.data.get("data_points")
        product_type = request.data.get("product_type")
        if not (data_points and product_type):
            return Response(
                {"error": "Missing required fields."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        api_key = os.environ.get("GEMINI_API_KEY")
        prompt = f"Based on the provided data {data_points}, predict the optimal pricing for {product_type} to maximize sales and profit. Consider factors like supply and demand, competitor pricing, and consumer trends. Provide a recommended price range and a brief rationale."
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
            params={"key": api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]},
        )
        if response.status_code == 200:
            result = response.json()
            return Response({"result": result}, status=200)
        return Response({"error": "AI service failed."}, status=500)
