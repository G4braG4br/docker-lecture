from django.urls import re_path

from photition_notice import consumers

notice_urlpatterns = [
    re_path(r"ws/notice/$", consumers.NoticeConsumer.as_asgi()),
]
