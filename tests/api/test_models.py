import datetime

import pytest
from hypothesis import given
from hypothesis.extra import django

from api import models


@pytest.mark.django_db
class HypothesisApiModelTestCase(django.TestCase):
    @given(django.from_model(models.Area))
    def test_is_area(self, area_instance):
        self.assertIsInstance(area_instance, models.Area)
        self.assertIsNotNone(area_instance.pk)
        self.assertIsInstance(str(area_instance), str)
        self.assertIsInstance(repr(area_instance), str)

    @given(django.from_model(models.Category))
    def test_is_category(self, category_instance):
        self.assertIsInstance(category_instance, models.Category)
        self.assertIsNotNone(category_instance.pk)
        self.assertIsInstance(str(category_instance), str)
        self.assertIsInstance(repr(category_instance), str)

    @given(django.from_model(models.Certificate))
    def test_is_certificate(self, certificate_instance):
        self.assertIsInstance(certificate_instance, models.Certificate)
        self.assertIsNotNone(certificate_instance.pk)
        self.assertIsInstance(str(certificate_instance), str)
        self.assertIsInstance(repr(certificate_instance), str)


@pytest.mark.django_db
def test_business_str(business):
    business.save()

    assert business.pk is not None
    assert isinstance(str(business), str)
    assert isinstance(repr(business), str)


@pytest.mark.django_db
def test_joblisting_str(job_listing):
    job_listing.save()

    assert job_listing.pk is not None
    assert isinstance(str(job_listing), str)
    assert isinstance(repr(job_listing), str)


@pytest.mark.django_db
def test_joblisting_status(job_listing):
    job_listing.save()

    assert job_listing.pk is not None
    assert job_listing.status


@pytest.mark.django_db
def test_joblisting_status_inactive(
    job_listing_factory,
):
    the_past = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(weeks=1)
    job_listing = job_listing_factory(listing_expiry=the_past)
    job_listing.save()
    assert not job_listing.status


@pytest.mark.django_db
def test_jobapplication_str(job_application):
    job_application.save()

    assert job_application.pk is not None
    assert isinstance(str(job_application), str)
    assert isinstance(repr(job_application), str)
