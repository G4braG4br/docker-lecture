from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from photition_models.models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "photo_thumbnail_display")
    list_filter = ("created",)
    search_fields = (
        "event",
        "recipient__username",
    )
    readonly_fields = ("created",)

    def photo_thumbnail_display(self, obj):
        if obj.photo and obj.photo.photo_thumbnail:
            return mark_safe("<img src='%s'/>" % obj.photo.photo_thumbnail.url)
        return _("No photo")
