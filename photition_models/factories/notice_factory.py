import factory

from photition_models.models import Notice


class NoticeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notice
