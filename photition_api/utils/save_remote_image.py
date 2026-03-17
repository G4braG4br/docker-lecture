import os
from urllib.parse import urlparse

import requests
from django.core.files.base import ContentFile

from photition_models.models import PhotitionUser


def save_remote_image(instance, url):
    response = requests.get(url)
    response.raise_for_status()

    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path) or "image.jpg"

    if isinstance(instance, PhotitionUser):
        instance.avatar.save(filename, ContentFile(response.content), save=True)
    else:
        instance.photo.save(filename, ContentFile(response.content), save=True)
    instance.save()
