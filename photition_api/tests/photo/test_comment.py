from django.urls import reverse
from rest_framework import status

from photition_api.tests.photo.photo_test_case import PhotoAPITestCase
from photition_models.factories import PhotitionUserFactory, PhotoFactory


class CommentTestCase(PhotoAPITestCase):
    def setUp(self):
        self.user = PhotitionUserFactory.create()
        self.photo = PhotoFactory.create(author=self.user)

        self.request_data = {
            "comment": "test",
        }

        self.url = reverse("comment", kwargs={"id": self.photo.id})

    def test_comment_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.request_data)
        self.assertEqual(status.is_success(response.status_code), True)
