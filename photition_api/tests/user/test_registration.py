from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from photition_api.utils.disable_error_decorator import disable_error_logger_level


class RegistrationTestCase(APITestCase):
    def setUp(self):
        self.data = {
            "username": "test",
            "email": "test@example.com",
            "password": "password",
        }
        self.url = reverse("registration")

    def test_registration_201(self):
        response = self.client.post(self.url, data=self.data, format="json")
        self.assertEqual(status.is_success(response.status_code), True)

    @disable_error_logger_level
    def test_registration_duplicate_400(self):
        self.client.post(self.url, data=self.data, format="json")
        response = self.client.post(self.url, data=self.data, format="json")
        self.assertEqual(status.is_success(response.status_code), False)
