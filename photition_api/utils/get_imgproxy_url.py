import base64
import hashlib
import hmac

from decouple import config

IMGPROXY_HOST = config("IMGPROXY_HOST", "127.17.0.0")
IMGPROXY_KEY = config("IMGPROXY_KEY", "test")
IMGPROXY_SALT = config("IMGPROXY_SALT", "test")


def get_imgproxy_url(target: str):
    key = bytes.fromhex(IMGPROXY_KEY)
    salt = bytes.fromhex(IMGPROXY_SALT)

    target = target.lstrip("/")
    if target.startswith("media/"):
        target = target.replace("media/", "", 1)

    source_url = f"local:///{target}"
    encoded_url = base64.urlsafe_b64encode(source_url.encode()).rstrip(b"=").decode()

    path = "/rs:{resize}:{width}:{height}/g:{gravity}/el:{enlarge}/{encoded_url}.{extension}".format(
        encoded_url=encoded_url,
        resize="fill",
        width=300,
        height=300,
        gravity="no",
        enlarge=1,
        extension="jpg",
    ).encode()
    digest = hmac.new(key, msg=salt + path, digestmod=hashlib.sha256).digest()

    protection = base64.urlsafe_b64encode(digest).rstrip(b"=")

    url = b"/%s%s" % (
        protection,
        path,
    )

    return url.decode()
