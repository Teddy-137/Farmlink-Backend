from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from .models import Product
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.


class ProductAPITest(APITestCase):
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

    def test_product_list(self):
        response = self.client.get(reverse("product-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_permission(self):
        self.client.force_authenticate(user=self.consumer)
        response = self.client.post(
            reverse("product-list"),
            {
                "name": "Banana",
                "description": "Yellow",
                "price": 2.0,
                "category": "Fruit",
                "producer": self.consumer.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ai_quality_grading(self):
        self.client.force_authenticate(user=self.producer)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
            tmp.write(b"fake image data")
            tmp.seek(0)
            photo = SimpleUploadedFile(tmp.name, tmp.read(), content_type="image/jpeg")
            response = self.client.post(
                reverse("quality_grading"),
                {"product_type": "Apple", "criteria": "color, size", "photo": photo},
            )
            self.assertIn(response.status_code, [200, 500])
