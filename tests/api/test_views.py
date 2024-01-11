import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework_serializer_extensions import utils

from api.models import Area, Category, JobListing
from api.views import AreaViewSet, CategoryViewSet, JobListingViewSet


@pytest.mark.django_db
def test_area_list(api_rf, areas):
    request = api_rf.get(reverse("area-list"))
    area_list = AreaViewSet.as_view({"get": "list"})
    response = area_list(request)
    assert response.data["count"] == Area.objects.count()


@pytest.mark.django_db
def test_area_detail(api_rf, areas):
    request = api_rf.get(reverse("area-detail", args=[areas[0].pk]))
    area_detail = AreaViewSet.as_view({"get": "retrieve"})
    response = area_detail(request, pk=areas[0].pk)
    assert response.data["id"] == areas[0].pk
    assert response.data["name"] == areas[0].name
    assert response.data["state"] == areas[0].state


@pytest.mark.django_db
def test_category_list(api_rf):
    request = api_rf.get(reverse("category-list"))
    category_list = CategoryViewSet.as_view({"get": "list"})
    response = category_list(request)
    assert response.data["count"] == Category.objects.count()


@pytest.mark.django_db
def test_category_detail(api_rf):
    cat_1 = Category.objects.first()
    request = api_rf.get(reverse("category-detail", args=[cat_1.pk]))
    category_detail = CategoryViewSet.as_view({"get": "retrieve"})
    response = category_detail(request, pk=cat_1.pk)
    assert response.data["id"] == cat_1.pk
    assert response.data["name"] == cat_1.name


@pytest.mark.django_db
def test_job_listing_list(api_rf, job_listings):
    request = api_rf.get(reverse("job-listing-list"))
    job_listing_list = JobListingViewSet.as_view({"get": "list"})
    response = job_listing_list(request)
    assert (
        response.data["count"]
        == JobListing.objects.filter(listing_expiry__gt=timezone.now()).count()
    )


@pytest.mark.django_db
def test_job_listing_list_by_area(api_rf, job_listings):
    area_id = job_listings[0].business.area.pk
    request = api_rf.get(reverse("job-listing-list"), {"area": area_id})
    job_listing_list = JobListingViewSet.as_view({"get": "list"})
    response = job_listing_list(request)
    assert (
        response.data["count"]
        == JobListing.objects.filter(listing_expiry__gt=timezone.now())
        .filter(business__area__pk=area_id)
        .count()
    )


@pytest.mark.django_db
def test_job_listing_list_by_category(api_rf, job_listings):
    category_id = job_listings[0].category.pk
    request = api_rf.get(reverse("job-listing-list"), {"category": category_id})
    job_listing_list = JobListingViewSet.as_view({"get": "list"})
    response = job_listing_list(request)
    assert (
        response.data["count"]
        == JobListing.objects.filter(listing_expiry__gt=timezone.now())
        .filter(category__pk=category_id)
        .count()
    )


@pytest.mark.django_db
def test_job_listing_list_by_type(api_rf, job_listings):
    position_type = job_listings[0].position_type
    request = api_rf.get(reverse("job-listing-list"), {"position_type": position_type})
    job_listing_list = JobListingViewSet.as_view({"get": "list"})
    response = job_listing_list(request)
    assert (
        response.data["count"]
        == JobListing.objects.filter(listing_expiry__gt=timezone.now())
        .filter(position_type=position_type)
        .count()
    )
