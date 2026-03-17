from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from photition_api.utils.upload_file import (
    save_file,
    skip_saving_file,
    uploaded_file_path,
)
from photition_models.models.user.managers.photitionuser_manager import (
    PhotitionUserManager,
)


class PhotitionUser(AbstractUser):

    objects = PhotitionUserManager()

    email = models.EmailField(
        unique=True,
        verbose_name=_("Email"),
        help_text=_("Email"),
    )
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to=uploaded_file_path,
        verbose_name=_("Avatar"),
        help_text=_("Avatar"),
    )
    avatar_thumbnail = ImageSpecField(
        source="avatar",
        processors=[ResizeToFill(50, 50)],
        format="JPEG",
        options={"quality": 60},
    )


pre_save.connect(skip_saving_file, sender=PhotitionUser)
post_save.connect(save_file, sender=PhotitionUser)
