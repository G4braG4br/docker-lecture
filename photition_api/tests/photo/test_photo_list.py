from django.urls import reverse
from rest_framework import status

from photition_api.tests.photo.photo_test_case import PhotoAPITestCase
from photition_models.factories import PhotitionUserFactory


class PhotoListTestCase(PhotoAPITestCase):
    def setUp(self):
        self.user = PhotitionUserFactory.create()
        self.url = reverse(
            "photo_list", query={"page": "1", "per_page": "10", "search": "test"}
        )

    def test_photo_list_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(status.is_success(response.status_code), True)
