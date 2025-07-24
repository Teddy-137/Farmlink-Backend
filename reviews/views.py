from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.exceptions import PermissionDenied

# Create your views here.


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["product__name", "consumer__username"]

    def perform_create(self, serializer):
        if self.request.user.role != "consumer":
            raise PermissionDenied("Only consumers can create reviews.")
        serializer.save(consumer=self.request.user)

    def get_queryset(self):
        if self.request.user.role == "producer":
            return Review.objects.all()
        return Review.objects.filter(consumer=self.request.user)
