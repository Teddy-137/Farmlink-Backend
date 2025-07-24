from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Order
from .serializers import OrderSerializer
from rest_framework.exceptions import PermissionDenied

# Create your views here.


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["consumer__username", "status"]
    ordering_fields = ["created_at", "status"]

    def perform_create(self, serializer):
        if self.request.user.role != "consumer":
            raise PermissionDenied("Only consumers can create orders.")
        serializer.save(consumer=self.request.user)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if request.user.role == "producer" and not any(
            p.producer == request.user for p in order.products.all()
        ):
            raise PermissionDenied("Producers can only update their own orders.")
        return super().update(request, *args, **kwargs)
