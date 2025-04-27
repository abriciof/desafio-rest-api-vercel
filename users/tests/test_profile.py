from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileTests(APITestCase):

    def setUp(self):
        self.url = reverse('user-me')

    def create_user_and_login(self):
        user = User.objects.create_user(username="testuser", email="test@example.com", password="Password123")
        user.email_confirmed = True
        user.save()
        login_response = self.client.post(reverse('auth-login'), {"username": "testuser", "password": "Password123"}, format='json')
        token = login_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return user

    def test_retrieve_profile(self):
        self.create_user_and_login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("username", response.data)

    def test_update_profile(self):
        self.create_user_and_login()
        response = self.client.patch(self.url, {"first_name": "John", "last_name": "Doe"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "John")
