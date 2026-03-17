from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Prefetch


class PhotoManager(models.QuerySet):
    def safe_get(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def with_prefetch_comments(self):
        from photition_models.models.comment.models import Comment

        return self.all().prefetch_related(
            Prefetch(
                "comments", Comment.objects.filter(is_deleted=False, belongs_to=None)
            ),
            Prefetch("comments__belongs", Comment.objects.filter(is_deleted=False)),
        )
