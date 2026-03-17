from decouple import config
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from photition.settings.django import BASE_URL
from photition_api.serializers.user.user import ListUserSerializer
from photition_api.utils.get_imgproxy_url import get_imgproxy_url
from photition_models.models import PhotoStats
from photition_models.models.photo.photo_model import Photo


class PhotoListSerializer(serializers.ModelSerializer):
    comment_count = SerializerMethodField()
    vote_count = SerializerMethodField()
    is_voted = serializers.BooleanField(read_only=True)
    author = ListUserSerializer(read_only=True)
    prev_photo = SerializerMethodField()
    photo_thumbnail = SerializerMethodField()

    class Meta:
        model = Photo
        fields = (
            "id",
            "photo_thumbnail",
            "title",
            "description",
            "comment_count",
            "vote_count",
            "is_voted",
            "author",
            "prev_photo",
            "state",
            "created_at",
        )

    def get_prev_photo(self, obj):
        if obj.prev_photo:
            return f"{BASE_URL}{obj.prev_photo.url}"
        return None

    def get_photo_thumbnail(self, obj):
        if obj.photo_thumbnail:
            return f"{BASE_URL}{obj.photo_thumbnail.url}"
        return None

    def get_comment_count(self, instance):
        return PhotoStats.objects.get(photo_id=instance.id).comment_count

    def get_vote_count(self, instance):
        return PhotoStats.objects.get(photo_id=instance.id).vote_count
