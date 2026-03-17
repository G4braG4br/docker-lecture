import factory

from photition_api.utils.get_test_image import get_test_image
from photition_models.models.user.photition_user_model import PhotitionUser


class PhotitionUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PhotitionUser

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")
    is_staff = False

    @factory.lazy_attribute
    def avatar(self):
        return get_test_image()
