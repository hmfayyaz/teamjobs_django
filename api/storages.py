import uuid
from pathlib import PurePath

from django.conf import settings
from django.core.files.storage import get_storage_class
from django.utils.deconstruct import deconstructible

CvWrappedStorage: type = get_storage_class(settings.CV_WRAPPED_STORAGE_CLASS)


def cv_upload_to(instance, filename: str) -> str:
    suffix = PurePath(filename).suffix or ""
    return f"job_listing_{instance.job_listing_id}/{uuid.uuid4()}{suffix}"


@deconstructible
class CvFileStorage(CvWrappedStorage):
    """Storage for application CVs, which shouldn't be public.

    Arguments are set as a dictionary in settings.CV_STORAGE_ARGS
    """

    def __init__(self):
        try:
            kwargs = settings.CV_STORAGE_ARGS
        except AttributeError:
            kwargs = {}
        super().__init__(**kwargs)
