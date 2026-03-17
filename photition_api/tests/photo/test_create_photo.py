from django.urls import reverse
from rest_framework import status

from photition_api.tests.photo.photo_test_case import PhotoAPITestCase
from photition_api.utils.get_test_image import get_test_image
from photition_models.factories import PhotitionUserFactory


class CreatePhotoTestCase(PhotoAPITestCase):
    def setUp(self):
        self.user = PhotitionUserFactory.create()

        self.request_data = {
            "title": "test",
            "description": "test",
            "photo": get_test_image(),
        }

        self.url = reverse("create_photo")

    def test_delete_comment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.request_data)
        self.assertEqual(status.is_success(response.status_code), True)
