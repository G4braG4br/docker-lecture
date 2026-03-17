from decouple import config
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from photition_api.serializers.comment.serializer import CommentSerializer
from photition_api.serializers.user.user import ListUserSerializer
from photition_models.models.comment.models import Comment
from photition_models.models.photo.materialized_views import PhotoStats
from photition_models.models.photo.photo_model import Photo


class PhotoSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    vote_count = SerializerMethodField()
    is_voted = serializers.BooleanField(read_only=True)
    author = ListUserSerializer(read_only=True)
    photo = SerializerMethodField()
    prev_photo = SerializerMethodField()
    photo_thumbnail = SerializerMethodField()
    comment_count = SerializerMethodField()

    class Meta:
        model = Photo
        fields = (
            "id",
            "photo",
            "photo_thumbnail",
            "title",
            "description",
            "comment_count",
            "comments",
            "vote_count",
            "is_voted",
            "author",
            "prev_photo",
            "state",
            "created_at",
        )

    def get_photo(self, obj):
        if obj.photo:
            from photition.settings.django import BASE_URL

            return f"{BASE_URL}{obj.photo.url}"
        return None

    def get_prev_photo(self, obj):
        if obj.prev_photo:
            from photition.settings.django import BASE_URL

            return f"{BASE_URL}{obj.prev_photo.url}"
        return None

    def get_photo_thumbnail(self, obj):
        if obj.photo_thumbnail:
            from photition.settings.django import BASE_URL

            return f"{BASE_URL}{obj.photo_thumbnail.url}"
        return None

    def get_vote_count(self, instance):
        return PhotoStats.objects.get(photo_id=instance.id).vote_count

    def get_comment_count(self, instance):
        return PhotoStats.objects.get(photo_id=instance.id).comment_count
