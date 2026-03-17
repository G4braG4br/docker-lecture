from rest_framework import status
from service_objects_autodocs.auto_parameters_spectacular import (
    prepare_parameters_for_docs,
    prepare_request_body_for_docs,
)
from service_objects_autodocs.exceptions import (
    get_validation_error_yasg_response,
)

from photition_api.serializers.comment.serializer import CommentSerializer
from photition_api.serializers.photo import PhotoListSerializer, PhotoSerializer
from photition_api.services.photo import (
    CommentService,
    CreatePhotoService,
    DeleteCommentService,
    DeletePhotoService,
    GetDeletedPhotos,
    GetPhotoService,
    PhotoListService,
    RestorePhotoService,
    UpdateCommentService,
    UpdatePhotoService,
    VoteService,
)
from photition_api.services.photo.moderate_photo import ModeratePhoto

photo_list_doc: dict = {
    "tags": [
        "Photos",
    ],
    "summary": "Get photo list",
    "request": prepare_parameters_for_docs(PhotoListService, exclude=("user",)),
    "responses": {
        status.HTTP_200_OK: PhotoListSerializer(many=True),
        status.HTTP_400_BAD_REQUEST: get_validation_error_yasg_response,
    },
}

photo_detail_doc: dict = {
    "tags": [
        "Photos",
    ],
    "summary": "Get photo detail",
    "request": prepare_parameters_for_docs(GetPhotoService, exclude=("user",)),
    "responses": {
        status.HTTP_200_OK: PhotoSerializer,
        status.HTTP_400_BAD_REQUEST: get_validation_error_yasg_response,
    },
}

update_photo_doc: dict = {
    "tags": [
        "Photos",
    ],
    "summary": "Update photo",
    "request": prepare_request_body_for_docs(
        UpdatePhotoService,
        body_data_types=("multipart/form-data",),
    ),
    "responses": {
        status.HTTP_201_CREATED: PhotoSerializer,
        status.HTTP_400_BAD_REQUEST: get_validation_error_yasg_response,
    },
}

create_photo_doc: dict = {
    "tags": [
        "Photos",
    ],
    "summary": "Create photo",
    "request": prepare_request_body_for_docs(
        CreatePhotoService,
        exclude=("user",),
        body_data_types=("multipart/form-data",),
    ),
    "responses": {
        status.HTTP_201_CREATED: PhotoSerializer,
        status.HTTP_400_BAD_REQUEST: get_validation_error_yasg_response,
    },
}

create_comment_doc: dict = {
    "tags": [
        "Photos",
    ],
    "summary": "Create comment",
    "request": prepare_request_body_for_docs(CommentService, exclude=("user",)),
    "responses": {
        status.HTTP_201_CREATED: CommentSerializer,
        status.HTTP_400_BAD_REQUEST: get_validation_error_yasg_response,
    },
}

delete_photo_doc: dict = {
    "tags": [
        "Photos",
    ],
    "summary": "Delete photo",
    "request": prepare_request_body_for_docs(DeletePhotoService),
    "responses": {
        status.HTTP_200_OK: None,
        status.HTTP_400_BAD_REQUEST: get_validation_error_yasg_response,
    },
}

restore_photo_doc: dict = {
    "tags": [
        "Photos",
    ],
    "summary": "Restore photo",
    "request": prepare_request_body_for_docs(RestorePhotoService),
    "responses": {
        status.HTTP_200_OK: PhotoSerializer,
        status.HTTP_400_BAD_REQUEST: get_validation_error_yasg_response,
    },
}

moderate_photo_doc: dict = {
    "tags": [
        "Photos",
    ],
    "summary": "Moderate photo",
    "request": prepare_request_body_for_docs(ModeratePhoto, exclude=("user",)),
    "responses": {
        status.HTTP_200_OK: PhotoSerializer,
        status.HTTP_400_BAD_REQUEST: get_validation_error_yasg_response,
    },
}

vote_doc: dict = {
    "tags": [
        "Photos",
    ],
    "summary": "Vote for photo",
    "request": prepare_request_body_for_docs(VoteService, exclude=("user",)),
    "responses": {
        status.HTTP_200_OK: None,
        status.HTTP_400_BAD_REQUEST: get_validation_error_yasg_response,
    },
}

delete_comment_doc: dict = {
    "tags": [
        "Photos",
    ],
    "summary": "Delete comment",
    "request": prepare_request_body_for_docs(DeleteCommentService),
    "responses": {
        status.HTTP_200_OK: None,
        status.HTTP_400_BAD_REQUEST: get_validation_error_yasg_response,
    },
}

update_comment_doc: dict = {
    "tags": [
        "Photos",
    ],
    "summary": "Update comment",
    "request": prepare_request_body_for_docs(UpdateCommentService),
    "responses": {
        status.HTTP_201_CREATED: CommentSerializer,
        status.HTTP_400_BAD_REQUEST: get_validation_error_yasg_response,
    },
}

get_restore_photos_doc: dict = {
    "tags": [
        "Photos",
    ],
    "summary": "Get photos to restore",
    "request": prepare_parameters_for_docs(GetDeletedPhotos, exclude=("user",)),
    "responses": {
        status.HTTP_200_OK: PhotoListSerializer(many=True),
        status.HTTP_400_BAD_REQUEST: get_validation_error_yasg_response,
    },
}
