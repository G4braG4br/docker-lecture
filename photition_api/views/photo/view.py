from drf_spectacular.utils import extend_schema
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from photition_api.docs.photos.docs import (
    create_comment_doc,
    create_photo_doc,
    delete_comment_doc,
    delete_photo_doc,
    get_restore_photos_doc,
    moderate_photo_doc,
    photo_detail_doc,
    photo_list_doc,
    restore_photo_doc,
    update_comment_doc,
    update_photo_doc,
    vote_doc,
)
from photition_api.permissions.permissions import IsOwner
from photition_api.serializers.comment.serializer import CommentSerializer
from photition_api.serializers.photo import PhotoListSerializer, PhotoSerializer
from photition_api.services.photo import (
    CommentService,
    CreatePhotoService,
    DeleteCommentService,
    DeletePhotoService,
    GetPhotoService,
    PhotoListService,
    RestorePhotoService,
    UpdateCommentService,
    UpdatePhotoService,
    VoteService,
)
from photition_api.services.photo.get_deleted_photos import GetDeletedPhotos
from photition_api.services.photo.moderate_photo import ModeratePhoto
from photition_api.utils.custom_pagination import CustomPagination


class PhotoListView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(**photo_list_doc)
    def get(self, request, **kwargs):
        outcome = ServiceOutcome(
            PhotoListService,
            {
                **kwargs,
                **request.query_params.dict(),
                "user": request.user if request.user.is_authenticated else None,
            },
        )

        return Response(
            {
                "pagination": CustomPagination(
                    outcome.result,
                    current_page=outcome.service.cleaned_data["page"],
                    per_page=outcome.service.cleaned_data["per_page"],
                ).to_json(),
                "results": PhotoListSerializer(
                    outcome.result.object_list, many=True
                ).data,
            },
            status=outcome.response_status,
        )


class GetPhotoView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(**photo_detail_doc)
    def get(self, request, **kwargs):
        outcome = ServiceOutcome(
            GetPhotoService,
            {**kwargs, "user": request.user if request.user.is_authenticated else None},
        )

        return Response(
            PhotoSerializer(outcome.result).data, status=outcome.response_status
        )

    @extend_schema(**moderate_photo_doc)
    def patch(self, request, **kwargs):
        outcome = ServiceOutcome(
            ModeratePhoto,
            {
                **kwargs,
                **request.query_params.dict(),
                "user": request.user if request.user.is_authenticated else None,
            },
        )

        return Response(
            PhotoSerializer(outcome.result).data, status=outcome.response_status
        )


class CreatePhotoView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(**create_photo_doc)
    def post(self, request, **kwargs):
        outcome = ServiceOutcome(
            CreatePhotoService,
            {**kwargs, **request.data.dict(), "user": request.user},
            request.FILES,
        )

        return Response(
            PhotoSerializer(outcome.result).data, status=outcome.response_status
        )


class UpdatePhotoView(APIView):
    permission_classes = (IsAuthenticated, IsOwner)

    @extend_schema(**update_photo_doc)
    def patch(self, request, **kwargs):
        outcome = ServiceOutcome(
            UpdatePhotoService, {**request.data.dict(), **kwargs}, request.FILES
        )

        return Response(
            PhotoSerializer(outcome.result).data, status=outcome.response_status
        )


class DeletePhotoView(APIView):
    permission_classes = (IsAuthenticated, IsOwner)

    @extend_schema(**delete_photo_doc)
    def delete(self, request, **kwargs):
        outcome = ServiceOutcome(DeletePhotoService, {**kwargs})

        return Response(None, status=outcome.response_status)


class RestorePhotoView(APIView):
    permission_classes = (IsAuthenticated, IsOwner)

    @extend_schema(**restore_photo_doc)
    def post(self, request, **kwargs):
        outcome = ServiceOutcome(RestorePhotoService, {**kwargs})

        return Response(
            PhotoSerializer(outcome.result).data, status=outcome.response_status
        )


class GetDeletedPhotosView(APIView):
    permission_classes = (IsAuthenticated, IsOwner)

    @extend_schema(**get_restore_photos_doc)
    def get(self, request, **kwargs):
        outcome = ServiceOutcome(
            GetDeletedPhotos,
            {"user": request.user},
        )

        return Response(
            PhotoListSerializer(outcome.result, many=True).data,
            status=outcome.response_status,
        )


class VoteView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(**vote_doc)
    def post(self, request, **kwargs):
        outcome = ServiceOutcome(VoteService, {"user": request.user, **kwargs})

        return Response(None, status=outcome.response_status)


class CommentView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(**create_comment_doc)
    def post(self, request, **kwargs):
        outcome = ServiceOutcome(
            CommentService, {**kwargs, **request.data, "user": request.user}
        )

        return Response(
            CommentSerializer(outcome.result).data, status=outcome.response_status
        )


class UpdateCommentView(APIView):
    permission_classes = (IsAuthenticated, IsOwner)

    @extend_schema(**update_comment_doc)
    def patch(self, request, **kwargs):
        outcome = ServiceOutcome(UpdateCommentService, {**kwargs, **request.data})

        return Response(
            CommentSerializer(outcome.result).data, status=outcome.response_status
        )


class DeleteCommentView(APIView):
    permission_classes = (IsAuthenticated, IsOwner)

    @extend_schema(**delete_comment_doc)
    def delete(self, request, **kwargs):
        outcome = ServiceOutcome(DeleteCommentService, {**kwargs})

        return Response(None, status=outcome.response_status)
