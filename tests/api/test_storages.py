import pytest
from django.core.files.storage import get_storage_class

from api import storages

FROZEN_UUID = "00000000-0000-0000-0000-000000000000"


@pytest.mark.django_db
def test_cv_upload_to(job_application, freeze_uuids):
    upload_to = storages.cv_upload_to(job_application, "my-resume.pdf")
    expected = f"job_listing_{job_application.job_listing_id}/{FROZEN_UUID}.pdf"
    assert upload_to == expected


def test_cv_file_storage(settings):
    cv_storage = storages.CvFileStorage()
    storage_class = get_storage_class(settings.CV_WRAPPED_STORAGE_CLASS)
    assert issubclass(cv_storage.__class__, storage_class)


def test_cv_file_storage_no_args(settings):
    try:
        del settings.CV_STORAGE_ARGS
    except AttributeError:
        pass
    cv_storage = storages.CvFileStorage()
    assert isinstance(cv_storage, storages.CvFileStorage)
