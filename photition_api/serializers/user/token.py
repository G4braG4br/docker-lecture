from rest_framework import serializers

from photition_models.models.user.photition_session_model import PhotitionSession


class SessionTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotitionSession
        fields = ("session_token",)
