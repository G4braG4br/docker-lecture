from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from photition_api.docs.notice.docs import delete_notice_doc, get_notices_doc
from photition_api.serializers.notice.serializer import NoticeSerializer
from photition_api.services.notice.delete_notice import DeleteNoticeService
from photition_api.services.notice.get_notices import GetNoticesService


class NoticeListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(**get_notices_doc)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(GetNoticesService, {**kwargs, "user": request.user})

        return Response(
            NoticeSerializer(
                outcome.result, many=True, context={"request": request}
            ).data,
            status=outcome.response_status,
        )


class DeleteNotice(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(**delete_notice_doc)
    def delete(self, request, *args, **kwargs):
        outcome = ServiceOutcome(DeleteNoticeService, {**kwargs, "user": request.user})

        return Response(None, status=outcome.response_status)
