from django.contrib import admin

from photition_models.models import PhotitionUser


@admin.register(PhotitionUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "username")
    search_fields = (
        "username",
        "email",
    )
    list_filter = ("is_staff", "last_login")
    readonly_fields = ("is_staff", "last_login", "date_joined", "avatar")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False)
