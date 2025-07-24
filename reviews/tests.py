from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from products.models import Product
from .models import Review

# Create your tests here.


class ReviewAPITest(APITestCase):
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

    def test_create_review(self):
        response = self.client.post(
            reverse("review-list"),
            {"product": self.product.id, "rating": 5, "comment": "Great!"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_review_permission(self):
        self.client.force_authenticate(user=self.producer)
        response = self.client.post(
            reverse("review-list"),
            {"product": self.product.id, "rating": 5, "comment": "Great!"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
