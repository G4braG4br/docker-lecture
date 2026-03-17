from decouple import config

from photition_models.models.photo.photo_model import ALLOWED_IMAGE_EXTENSIONS

MAX_IMAGE_SIZE = int(config("MAX_IMAGE_SIZE", 100000))


def validate_file(file) -> bool:
    file_size = file.size
    file_extension = file.name.split(".")[-1]

    size = file_size < MAX_IMAGE_SIZE
    extension = file_extension in ALLOWED_IMAGE_EXTENSIONS

    return size and extension
