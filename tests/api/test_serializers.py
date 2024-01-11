import json

import pytest
from rest_framework.renderers import JSONRenderer

from api import serializers


@pytest.mark.django_db
def test_area_serializer(area):
    area_s = serializers.AreaSerializer(area)

    assert area.id == area_s.data["id"]
    assert area.name == area_s.data["name"]


@pytest.mark.django_db
def test_business_serializer(business):
    business_s = serializers.BusinessInJobListingSerializer(business)
    assert business.name == business_s.data["name"]
    business_location = {}
    for k in ["suburb", "state", "country", "line_1"]:
        business_location[k] = business.address[k]
    assert business_location == business_s.data["address"]
    assert "contact" not in business_s.data
    assert "owners" not in business_s.data


@pytest.mark.django_db
def test_joblisting_serializer(job_listing):
    job_listing.description = "<div>hello</div>"
    job_listing_s = serializers.JobListingSerializer(job_listing)
    job_listing_rt = json.loads(JSONRenderer().render(job_listing_s.data))
    assert job_listing_rt["description"] == "<div>hello</div>"
    assert (
        len(job_listing_rt["certificates_required"])
        == job_listing.certificates_required.count()
    )
    for cert in job_listing_rt["certificates_required"]:
        assert job_listing.certificates_required.filter(pk=cert["id"]).exists()

    assert job_listing_rt["category"]["id"] == job_listing.category.id


@pytest.mark.django_db
def test_job_application_serializer(job_application):
    job_application_s = serializers.JobApplicationSerializer(job_application)
    assert job_application_s.data["id"] == job_application.id
    assert job_application_s.data["job_listing"]["id"] == job_application.job_listing.pk
