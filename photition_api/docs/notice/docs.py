from rest_framework import status
from service_objects_autodocs.auto_parameters_spectacular import (
    prepare_parameters_for_docs,
    prepare_request_body_for_docs,
)
from service_objects_autodocs.exceptions import get_validation_error_yasg_response

from photition_api.serializers.notice.serializer import NoticeSerializer
from photition_api.services.notice.delete_notice import DeleteNoticeService
from photition_api.services.notice.get_notices import GetNoticesService

get_notices_doc: dict = {
    "tags": [
        "Notices",
    ],
    "summary": "Get notices",
    "request": prepare_parameters_for_docs(GetNoticesService, exclude=("user",)),
    "responses": {
        status.HTTP_200_OK: NoticeSerializer(many=True),
        status.HTTP_400_BAD_REQUEST: get_validation_error_yasg_response,
    },
}

delete_notice_doc: dict = {
    "tags": [
        "Notices",
    ],
    "summary": "Delete notice",
    "request": prepare_request_body_for_docs(DeleteNoticeService, exclude=("user",)),
    "responses": {
        status.HTTP_200_OK: None,
        status.HTTP_400_BAD_REQUEST: get_validation_error_yasg_response,
    },
}
