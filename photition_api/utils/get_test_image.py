from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


def get_test_image():
    img = Image.new("RGB", (100, 100), (0, 255, 0))
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_byte_arr = img_byte_arr.getvalue()

    return SimpleUploadedFile(
        name="test.jpg", content=img_byte_arr, content_type="image/jpg"
    )
