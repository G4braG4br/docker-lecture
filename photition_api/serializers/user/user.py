from decouple import config
from rest_framework import serializers

from photition_api.serializers.user.token import SessionTokenSerializer
from photition_models.models.user.photition_user_model import PhotitionUser


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(default="")
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = PhotitionUser
        fields = (
            "id",
            "username",
            "email",
            "is_active",
            "date_joined",
            "avatar",
            "is_staff",
            "token",
        )

    def get_token(self, user):
        session = user.sessions.first()
        if session:
            return SessionTokenSerializer(session).data["session_token"]
        return None

    def get_avatar(self, user):
        if user.avatar:
            from photition.settings.django import BASE_URL

            return f"{BASE_URL}{user.avatar.url}"
        return None


class ListUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = PhotitionUser
        fields = ("id", "username", "email", "is_active", "date_joined", "avatar")

    def get_avatar(self, user):
        if user.avatar:
            from photition.settings.django import BASE_URL

            return f"{BASE_URL}{user.avatar.url}"
        return None
