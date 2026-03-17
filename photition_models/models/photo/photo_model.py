from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from photition_api.utils.upload_file import (
    save_file,
    skip_saving_file,
    uploaded_file_path,
)
from photition_models.models.photo.managers import PhotoManager

ALLOWED_IMAGE_EXTENSIONS = (
    "jpg",
    "jpeg",
    "png",
)


class Photo(models.Model):

    objects = PhotoManager.as_manager()

    class Statuses(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        APPROVED = "APPROVED", _("Approved")
        REJECTED = "REJECTED", _("Rejected")

    photo = models.ImageField(
        upload_to=uploaded_file_path,
        verbose_name=_("Photo"),
        help_text=_("Photo"),
    )
    photo_thumbnail = ImageSpecField(
        source="photo",
        processors=[ResizeToFill(50, 50)],
        format="JPEG",
        options={"quality": 60},
    )
    title = models.CharField(
        max_length=50,
        verbose_name=_("Title"),
        help_text=_("Title"),
    )
    description = models.TextField(
        null=True,
        blank=True,
        max_length=1000,
        verbose_name=_("Description"),
        help_text=_("Description"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
        help_text=_("Updated at"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
        help_text=_("Created at"),
    )
    author = models.ForeignKey(
        "photition_models.PhotitionUser",
        on_delete=models.CASCADE,
        related_name="photos",
        related_query_name="photo",
        verbose_name=_("Author"),
        help_text=_("Author"),
    )
    votes = models.ManyToManyField("photition_models.PhotitionUser", through="Vote")
    is_allowed = models.BooleanField(
        default=False,
        verbose_name=_("Is allowed"),
        help_text=_("Is allowed"),
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_("Is deleted"),
        help_text=_("Is deleted"),
    )
    will_deleted_in = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Will deleted in"),
        help_text=_("Will deleted in"),
    )
    prev_photo = models.ImageField(
        null=True,
        blank=True,
        verbose_name=_("Previous photo"),
        help_text=_("Previous photo"),
    )
    prev_photo_thumbnail = ImageSpecField(
        source="prev_photo",
        processors=[ResizeToFill(50, 50)],
        format="JPEG",
        options={"quality": 60},
    )

    state = FSMField(
        default=Statuses.PENDING,
        choices=Statuses.choices,
        verbose_name=_("State"),
        help_text=_("State"),
    )

    @transition(
        field=state,
        source=Statuses.PENDING,
        target=Statuses.APPROVED,
        permission=lambda instance, user: user.is_staff,
    )
    def approve(self):
        self.is_allowed = True
        return True

    @transition(
        field=state,
        source="*",
        target=Statuses.REJECTED,
        permission=lambda instance, user: user.is_staff
        or instance.author.id == user.id,
    )
    def reject(self):
        self.is_allowed = False
        return True

    @transition(
        field=state,
        source="*",
        target=Statuses.PENDING,
        permission=lambda instance, user: user.is_staff
        or instance.author.id == user.id,
    )
    def roll_back(self):
        self.is_deleted = False
        self.is_allowed = False
        return True

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = (_("Photo"),)
        verbose_name_plural = _("Photos")


pre_save.connect(skip_saving_file, sender=Photo)
post_save.connect(save_file, sender=Photo)
