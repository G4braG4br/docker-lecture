import factory

from photition_models.factories.photo_factory import PhotoFactory
from photition_models.factories.user_factory import PhotitionUserFactory
from photition_models.models.comment.models import Comment


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    comment = factory.Faker("sentence", nb_words=3)
    author = factory.SubFactory(PhotitionUserFactory)
    photo = factory.SubFactory(PhotoFactory)
