from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from photition_models.factories import PhotitionUserFactory


class RefreshTestCase(APITestCase):
    def setUp(self):
        self.user = PhotitionUserFactory.create()
        self.url = reverse("refresh")
        self.client.force_authenticate(user=self.user)

    def test_refresh_200(self):
        response = self.client.post(self.url)
        self.assertEqual(status.is_success(response.status_code), True)
