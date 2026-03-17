from rest_framework import serializers
from rest_framework.fields import BooleanField, SerializerMethodField

from photition_api.serializers.user import UserSerializer
from photition_models.models.comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    belongs_to = SerializerMethodField()
    answer_to = SerializerMethodField()
    author = UserSerializer(read_only=True)

    @property
    def _skip(self) -> bool:
        return bool(self.context.get("skip", False))

    def get_belongs_to(self, obj):
        if obj.belongs_to is None and not self._skip:
            return CommentSerializer(
                obj.belongs, many=True, context={"skip": True}
            ).data
        return None

    def get_answer_to(self, obj):
        if obj.answer_to:
            return CommentSerializer(obj.answer_to, context={"skip": True}).data
        return None

    class Meta:
        model = Comment
        fields = "__all__"
