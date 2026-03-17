from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from photition_models.models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "photo_thumbnail_display",
    )
    list_filter = (
        "is_allowed",
        "is_deleted",
    )
    search_fields = (
        "title",
        "description",
        "author__username",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def photo_thumbnail_display(self, obj):
        if obj.photo_thumbnail:
            return mark_safe("<img src='%s'/>" % obj.photo_thumbnail.url)
        return _("No photo")
