import pytest

from api.factories.utils import joblistings


@pytest.mark.django_db
def test_create_duplicate_categories(settings):
    cats = joblistings.JobListingsManager.populate_categories(
        settings.API_FACTORY_PATHS["categories"]
    )
    assert len(cats) == 0


@pytest.mark.django_db
def test_create_duplicate_certificates(settings):
    certs = joblistings.JobListingsManager.populate_certificates(
        settings.API_FACTORY_PATHS["certificates"]
    )
    assert len(certs) == 0
