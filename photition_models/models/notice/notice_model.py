from django.db import models
from django.utils.translation import gettext_lazy as _


class Notice(models.Model):
    class Events(models.TextChoices):
        APPROVED = "APPROVED", _("Approved")
        REJECTED = "REJECTED", _("Rejected")
        GLOBAL = "GLOBAL", _("Global")
        NEW_VOTE = "NEW_VOTE", _("New Vote")
        VOTE_DELETED = "VOTE_DELETED", _("Vote Deleted")
        NEW_COMMENT = "NEW_COMMENT", _("New Comment")
        COMMENT_WILL_DELETED = "COMMENT_WILL_DELETED", _("Comment Will Deleted")

    initiator = models.ForeignKey(
        "photition_models.PhotitionUser",
        on_delete=models.CASCADE,
        null=True,
        related_name="initiator_notices",
        related_query_name="initiator_notice",
        verbose_name=_("Initiator"),
        help_text=_("Initiator"),
    )

    photo = models.ForeignKey(
        "photition_models.Photo",
        on_delete=models.SET_NULL,
        null=True,
        related_name="notices",
        related_query_name="notice",
        verbose_name=_("Photo"),
        help_text=_("Photo"),
    )
    recipient = models.ForeignKey(
        "photition_models.PhotitionUser",
        on_delete=models.CASCADE,
        null=True,
        related_name="notices",
        related_query_name="notice",
        verbose_name=_("Recipient"),
        help_text=_("Recipient"),
    )
    message = models.TextField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name=_("Message"),
        help_text=_("Message"),
    )
    numeric_data = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Numeric data"),
        help_text=_("Numeric data"),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created"),
        help_text=_("Created"),
    )
    event = models.CharField(
        default=Events.GLOBAL,
        choices=Events.choices,
        max_length=100,
        verbose_name=_("Event"),
        help_text=_("Event"),
    )

    def __str__(self):
        return self.event

    class Meta:
        verbose_name = _("Notice")
        verbose_name_plural = _("Notices")
