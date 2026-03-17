from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class PhotitionManager(models.QuerySet):
    def safe_get(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None
