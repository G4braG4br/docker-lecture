from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from photition_models.factories import PhotitionUserFactory


class GetUserTestCase(APITestCase):
    def setUp(self):
        self.user = PhotitionUserFactory.create()
        self.url = reverse("current")
        self.client.force_authenticate(user=self.user)

    def test_get_user_200(self):
        response = self.client.get(self.url)
        self.assertEqual(status.is_success(response.status_code), True)
