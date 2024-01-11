from django.urls import URLPattern, URLResolver, path
from rest_framework import routers

from .views import (
    AreaViewSet,
    CategoryViewSet,
    CreateBusinessView,
    CreateJobApplicationView,
    GetCertificateView,
    JobListingViewSet,
)

router = routers.DefaultRouter()

router.register(r"areas", AreaViewSet)
router.register(r"job-listings", JobListingViewSet, "job-listing")
router.register(r"categories", CategoryViewSet)
router.register(r"businesses", CreateBusinessView, "businesses"),

urlpatterns: list[URLPattern | URLResolver] = [
    path(r"job-applications", CreateJobApplicationView.as_view()),
    path(r"certificate", GetCertificateView.as_view()),
]

urlpatterns += router.urls
