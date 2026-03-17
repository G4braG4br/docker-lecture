from django.urls import path

from photition_api.views.photo.view import (
    CommentView,
    CreatePhotoView,
    DeleteCommentView,
    DeletePhotoView,
    GetDeletedPhotosView,
    GetPhotoView,
    PhotoListView,
    RestorePhotoView,
    UpdateCommentView,
    UpdatePhotoView,
    VoteView,
)

urlpatterns = [
    path("photos/", PhotoListView.as_view(), name="photo_list"),
    path("photos/create/", CreatePhotoView.as_view(), name="create_photo"),
    path("photos/<int:id>/", GetPhotoView.as_view(), name="photo"),
    path("photos/<int:id>/update/", UpdatePhotoView.as_view(), name="update_photo"),
    path("photos/<int:id>/delete/", DeletePhotoView.as_view(), name="delete_photo"),
    path("photos/<int:id>/restore/", RestorePhotoView.as_view(), name="restore_photo"),
    path("photos/restore/", GetDeletedPhotosView.as_view(), name="get_deleted_photos"),
    path(
        "photos/comment/update/<int:id>/",
        UpdateCommentView.as_view(),
        name="update_comment",
    ),
    path(
        "photos/comment/delete/<int:id>/",
        DeleteCommentView.as_view(),
        name="delete_comment",
    ),
    path("photos/<int:id>/vote/", VoteView.as_view(), name="vote"),
    path("photos/<int:id>/comment/", CommentView.as_view(), name="comment"),
]
