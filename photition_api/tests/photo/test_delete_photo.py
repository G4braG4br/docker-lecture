from django.urls import reverse
from rest_framework import status

from photition_api.tests.photo.photo_test_case import PhotoAPITestCase
from photition_models.factories import PhotitionUserFactory, PhotoFactory


class DeletePhotoTestCase(PhotoAPITestCase):
    def setUp(self):
        self.user = PhotitionUserFactory.create()
        self.photo = PhotoFactory.create(author=self.user)

        self.url = reverse("delete_photo", kwargs={"id": self.photo.id})

    def test_delete_photo_204(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(status.is_success(response.status_code), True)
