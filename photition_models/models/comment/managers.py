from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Prefetch


class CommentManager(models.QuerySet):
    def safe_get(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def with_prefetch_replies(self):
        return self.all().prefetch_related(
            Prefetch("belongs", self.filter(is_deleted=False))
        )
