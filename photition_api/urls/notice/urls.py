from django.urls import path

from photition_api.views.notice.view import DeleteNotice, NoticeListView

urlpatterns = [
    path("notice/", NoticeListView.as_view(), name="notice_list"),
    path("notice/<int:id>/delete/", DeleteNotice.as_view(), name="delete_notice"),
]
