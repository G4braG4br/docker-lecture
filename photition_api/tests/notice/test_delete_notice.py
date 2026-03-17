from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from photition_models.factories import NoticeStatusFactory, PhotitionUserFactory
from photition_models.factories.notice_factory import NoticeFactory


class DeleteNoticeTestCase(APITestCase):
    def setUp(self):
        self.user = PhotitionUserFactory.create()
        self.notice = NoticeFactory.create()
        self.notice_status = NoticeStatusFactory.create(
            user=self.user, notice=self.notice
        )
        self.url = reverse("delete_notice", kwargs={"id": self.notice.pk})
        self.client.force_authenticate(user=self.user)

    def test_delete_notice_200(self):
        response = self.client.delete(self.url)
        self.assertEqual(status.is_success(response.status_code), True)
