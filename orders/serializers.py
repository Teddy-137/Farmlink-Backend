from rest_framework import serializers
from .models import Order
from products.serializers import ProductSerializer
from products.models import Product


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True
    )
    consumer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["products"] = ProductSerializer(instance.products.all(), many=True).data
        return rep
