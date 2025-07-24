from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User


class UserAPITest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@example.com"
        )
        self.consumer = User.objects.create_user(
            username="consumer", password="pass", role="consumer"
        )
        self.client = APIClient()

    def test_register(self):
        response = self.client.post(
            reverse("register"),
            {"username": "newuser", "password": "pass", "role": "consumer"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        response = self.client.post(
            reverse("token_obtain_pair"), {"username": "consumer", "password": "pass"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_user_list_permission(self):
        self.client.force_authenticate(user=self.consumer)
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
