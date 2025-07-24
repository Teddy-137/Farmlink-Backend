from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from .models import Message

# Create your tests here.


class MessageAPITest(APITestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username="sender", password="pass", role="producer"
        )
        self.receiver = User.objects.create_user(
            username="receiver", password="pass", role="consumer"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.sender)

    def test_create_message(self):
        response = self.client.post(
            reverse("message-list"),
            {
                "sender": self.sender.id,
                "receiver": self.receiver.id,
                "content": "Hello",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
