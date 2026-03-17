from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from photition_models.factories import PhotitionUserFactory


class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = PhotitionUserFactory.create(
            password="password", email="test@example.com"
        )
        self.data = {
            "email": "test@example.com",
            "password": "password",
        }
        self.invalid_data = {
            "email": "tet@example.com",
            "password": "pasword",
        }
        self.url = reverse("login")

    def test_login_200(self):
        response = self.client.post(self.url, data=self.data, format="json")
        self.assertEqual(status.is_success(response.status_code), True)

    def test_login_invalid_data_400(self):
        response = self.client.post(self.url, data=self.invalid_data, format="json")
        self.assertEqual(status.is_success(response.status_code), False)
