from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from products.models import Product
from .models import Order

# Create your tests here.


class OrderAPITest(APITestCase):
    def setUp(self):
        self.producer = User.objects.create_user(
            username="producer", password="pass", role="producer"
        )
        self.consumer = User.objects.create_user(
            username="consumer", password="pass", role="consumer"
        )
        self.product = Product.objects.create(
            name="Apple",
            description="Fresh",
            price=1.0,
            category="Fruit",
            producer=self.producer,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.consumer)

    def test_create_order(self):
        response = self.client.post(
            reverse("order-list"),
            {"products": [self.product.id], "total_price": 1.0, "status": "pending"},
        )
        if response.status_code != status.HTTP_201_CREATED:
            print("RESPONSE DATA:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_permission(self):
        self.client.force_authenticate(user=self.producer)
        response = self.client.post(
            reverse("order-list"),
            {"products": [self.product.id], "total_price": 1.0, "status": "pending"},
        )
        if response.status_code != status.HTTP_403_FORBIDDEN:
            print("RESPONSE DATA:", response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
