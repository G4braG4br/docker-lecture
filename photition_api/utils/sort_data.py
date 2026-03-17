from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    SimpleUploadedFile,
    TemporaryUploadedFile,
    UploadedFile,
)


def sort_data(target, fields, file_fields) -> None:
    for key, value in target.items():
        if key != "user":
            if is_file(value):
                file_fields[key] = value
            else:
                fields[key] = value


def is_file(f) -> bool:
    return (
        isinstance(f, UploadedFile)
        or isinstance(f, InMemoryUploadedFile)
        or isinstance(f, TemporaryUploadedFile)
        or isinstance(f, SimpleUploadedFile)
    )
