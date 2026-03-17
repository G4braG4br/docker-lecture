from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from photition_api.utils.disable_error_decorator import disable_error_logger_level
from photition_api.utils.get_test_image import get_test_image
from photition_models.factories import PhotitionUserFactory


class UpdateUserTestCase(APITestCase):
    def setUp(self):
        self.first_request_data = {"username": "test2", "avatar": get_test_image()}
        self.second_request_data = {"avatar": get_test_image()}
        self.invalid_request_data = {
            "username": "test1",
        }
        self.user = PhotitionUserFactory.create()
        self.user2 = PhotitionUserFactory.create(username="test1")
        self.url = reverse("current")

    def test_update_user_200(self):
        self.client.force_authenticate(user=self.user)
        self.client.patch(self.url, data=self.first_request_data, format="multipart")
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(
            self.url, data=self.second_request_data, format="multipart"
        )
        self.assertEqual(status.is_success(response.status_code), True)

    @disable_error_logger_level
    def test_update_user_taken_username_400(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, data=self.invalid_request_data)
        self.assertEqual(status.is_success(response.status_code), False)
