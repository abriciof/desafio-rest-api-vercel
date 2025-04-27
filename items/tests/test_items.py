from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from items.models import Item

User = get_user_model()

class ItemsTests(APITestCase):

    def setUp(self):
        self.items_url = reverse('items-public')
        self.restricted_items_url = reverse('items-restricted')

    def create_items(self):
        owner = self.create_user()
        Item.objects.create(owner=owner, title="Item Público", body="Body 1", is_public=True)
        Item.objects.create(owner=owner, title="Item Restrito", body="Body 2", is_public=False)

    def create_user(self, email="item@example.com", password="senhadificil123"):
        user = User.objects.create_user(username="itemuser", email=email, password=password)
        user.email_confirmed = True
        user.save()
        return user

    def test_list_public_items(self):
        self.create_items()
        response = self.client.get(self.items_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_restricted_items_requires_auth(self):
        self.create_items()
        response = self.client.get(self.restricted_items_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_restricted_items_with_auth(self):
        user = self.create_user()
        login_response = self.client.post(reverse('auth-login'), {"username": "itemuser", "password": "senhadificil123"} , format='json')
        token = login_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.restricted_items_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
