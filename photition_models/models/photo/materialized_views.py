from django.db import models
from django_materialized_view.base_model import MaterializedViewModel


class PhotoStats(MaterializedViewModel):
    create_pkey_index = True

    class Meta:
        managed = False

    photo_id = models.OneToOneField(
        "photition_models.Photo",
        on_delete=models.DO_NOTHING,
        primary_key=True,
        db_column="photo_id",
        related_name="stats",
        related_query_name="stat",
    )
    comment_count = models.IntegerField()
    vote_count = models.IntegerField()

    @staticmethod
    def get_query_from_queryset():
        return (
            Photo.objects.values("id")
            .annotate(
                photo_id=models.F("id"),
                vote_count=models.Count("votes", distinct=True),
                comment_count=models.Count(
                    "comment", filter=models.Q(comment__is_deleted=False), distinct=True
                ),
            )
            .values("photo_id", "vote_count", "comment_count")
        )
