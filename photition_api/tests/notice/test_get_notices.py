from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from photition_models.factories import PhotitionUserFactory


class GetNoticesTestCase(APITestCase):
    def setUp(self):
        self.user = PhotitionUserFactory.create()
        self.url = reverse("notice_list")
        self.client.force_authenticate(user=self.user)

    def test_get_notices_200(self):
        response = self.client.get(self.url)
        self.assertEqual(status.is_success(response.status_code), True)
