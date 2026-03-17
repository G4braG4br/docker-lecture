from django.urls import reverse
from rest_framework import status

from photition_api.tests.photo.photo_test_case import PhotoAPITestCase
from photition_models.factories import PhotitionUserFactory
from photition_models.factories.comment_factory import CommentFactory


class DeleteCommentTestCase(PhotoAPITestCase):
    def setUp(self):
        self.user = PhotitionUserFactory.create()
        self.comment = CommentFactory.create(author=self.user)

        self.url = reverse("delete_comment", kwargs={"id": self.comment.id})

    def test_delete_comment_204(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(status.is_success(response.status_code), True)
