from django.urls import reverse
from rest_framework import status

from photition_api.tests.photo.photo_test_case import PhotoAPITestCase
from photition_api.utils.get_test_image import get_test_image
from photition_models.factories import PhotitionUserFactory, PhotoFactory


class UpdatePhotoTestCase(PhotoAPITestCase):
    def setUp(self):
        self.user = PhotitionUserFactory.create()
        self.photo = PhotoFactory.create(author=self.user)
        from photition_models.models.photo.materialized_views import PhotoStats

        PhotoStats.refresh()

        self.request_data = {
            "id": self.photo.id,
            "title": "test1",
            "description": "test1",
            "photo": get_test_image(),
        }

        self.url = reverse("update_photo", kwargs={"id": self.photo.id})

    def test_update_photo_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self.url, data=self.request_data, format="multipart"
        )
        self.assertEqual(status.is_success(response.status_code), True)
