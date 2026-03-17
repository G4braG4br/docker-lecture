from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from photition_models.models.comment.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "short_comment")
    list_filter = (
        "is_deleted",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "comment",
        "author__username",
        "photo__title",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    @admin.display(description=_("Short comment"))
    def short_comment(self, obj):
        return obj.comment[:50] + "..." if len(obj.comment) > 50 else obj.comment
