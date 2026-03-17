from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from photition_api.serializers.photo import PhotoListSerializer
from photition_api.serializers.user.user import ListUserSerializer
from photition_models.models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    photo = SerializerMethodField(read_only=True, required=False)
    initiator = ListUserSerializer(read_only=True, required=False)
    recipient = ListUserSerializer(read_only=True, required=False)

    class Meta:
        model = Notice
        fields = (
            "id",
            "initiator",
            "event",
            "recipient",
            "photo",
            "message",
            "numeric_data",
        )

    def get_photo(self, obj):
        if obj.photo:
            return PhotoListSerializer(obj.photo, context=self.context).data
        return None
