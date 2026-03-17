from django.urls import reverse
from rest_framework import status

from photition_api.tests.photo.photo_test_case import PhotoAPITestCase
from photition_models.factories import PhotitionUserFactory
from photition_models.factories.comment_factory import CommentFactory


class UpdateCommentTestCase(PhotoAPITestCase):
    def setUp(self):
        self.user = PhotitionUserFactory.create()
        self.comment = CommentFactory.create(author=self.user)
        from photition_models.models.photo.materialized_views import PhotoStats

        PhotoStats.refresh()

        self.request_data = {
            "comment": "test1",
        }

        self.url = reverse("update_comment", kwargs={"id": self.comment.id})

    def test_update_comment_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, data=self.request_data, format="json")
        self.assertEqual(status.is_success(response.status_code), True)
