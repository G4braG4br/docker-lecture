import functools
import logging


def disable_error_logger_level(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger("django.request")
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)
        value = func(*args, **kwargs)
        logger.setLevel(previous_level)
        return value

    return wrapper
