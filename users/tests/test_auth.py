from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()

class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('auth-register')
        self.login_url = reverse('auth-login')
        self.logout_url = reverse('auth-logout')
        self.change_password_url = reverse('auth-change-password')
        self.send_token_url = reverse('email-send-token')
        self.verify_token_url = reverse('email-verify-token')

    def create_user(self, email="test@example.com", password="senhadificil123"):
        user = User.objects.create_user(username="testuser", email=email, password=password)
        user.email_confirmed = True
        user.save()
        return user

    def test_user_registration(self):
        data = {
            "username": "usernovo",
            "email": "usernovo@example.com",
            "first_name": "User",
            "last_name": "Novo",
            "profile_image": "",
            "password": "senha123dificil",
            "password_confirm": "senha123dificil"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        self.create_user()
        data = {"username": "testuser", "password": "senhadificil123"}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_user_logout(self):
        user = self.create_user()
        login_response = self.client.post(self.login_url, {"username": "testuser", "password": "senhadificil123"}, format='json')
        token = login_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_change_password(self):
        user = self.create_user()
        login_response = self.client.post(self.login_url, {"username": "testuser", "password": "senhadificil123"}, format='json')
        token = login_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {"old_password": "senhadificil123", "new_password": "NewPassword789"}
        response = self.client.put(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('users.utils.emailer.send_confirmation_email')
    def test_send_email_token(self, mock_send_email):
        user = self.create_user()
        login_response = self.client.post(self.login_url, {"username": "testuser", "password": "senhadificil123"}, format='json')
        token = login_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.send_token_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_email_token_fail(self):
        # Sem token correto
        response = self.client.get(self.verify_token_url, {"email": "wrong@example.com", "token": "abc"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
