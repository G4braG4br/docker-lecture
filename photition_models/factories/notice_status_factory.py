import factory

from photition_models.factories.notice_factory import NoticeFactory
from photition_models.factories.user_factory import PhotitionUserFactory
from photition_models.models.notice.notice_status_model import NoticeStatus


class NoticeStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NoticeStatus

    notice = factory.SubFactory(NoticeFactory)
    user = factory.SubFactory(PhotitionUserFactory)
