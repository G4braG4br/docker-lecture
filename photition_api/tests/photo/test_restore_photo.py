from django.urls import reverse
from rest_framework import status

from photition_api.tests.photo.photo_test_case import PhotoAPITestCase
from photition_models.factories import PhotitionUserFactory, PhotoFactory


class RestorePhotoTestCase(PhotoAPITestCase):
    def setUp(self):
        self.user = PhotitionUserFactory.create()
        self.photo = PhotoFactory.create(author=self.user)
        from photition_models.models.photo.materialized_views import PhotoStats

        PhotoStats.refresh()

        self.url = reverse("restore_photo", kwargs={"id": self.photo.id})

    def test_restore_photo_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(status.is_success(response.status_code), True)
