import factory

from photition_api.utils.get_test_image import get_test_image
from photition_models.factories.user_factory import PhotitionUserFactory
from photition_models.models.photo.photo_model import Photo


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=3)
    author = factory.SubFactory(PhotitionUserFactory)

    @factory.lazy_attribute
    def photo(self):
        return get_test_image()
