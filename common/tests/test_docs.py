from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class DocsTests(APITestCase):

    def setUp(self):
        self.terms = reverse('terms-of-use')
        self.privacy = reverse('privacy-policy')

    def test_download_terms(self):
        response = self.client.get(self.terms)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_download_privacy_policy(self):
        response = self.client.get(self.privacy)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')
