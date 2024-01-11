from rest_framework import filters, generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Area, Business, Category, Certificate, JobApplication, JobListing
from .serializers import (
    AreaSerializer,
    CategorySerializer,
    CertificateSerializer,
    CreateBusinessSerializer,
    JobApplicationSerializer,
    JobListingSerializer,
)

# Create your views here.


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class JobListingViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = JobListingSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ["title", "description", "position_type"]

    def get_queryset(self):
        active = self.request.query_params.get("status", "active")
        category_param = self.request.query_params.get("category")
        area_param = self.request.query_params.get("area")
        position_param = self.request.query_params.get("position_type")
        match active:
            case "active":
                jobs = JobListing.objects.active().for_serialization()
            case "inactive":
                jobs = JobListing.objects.inactive().for_serialization()
            case _:
                jobs = JobListing.objects.all().for_serialization()

        if category_param is not None:
            jobs = jobs.filter(category__id=category_param)

        if area_param is not None:
            jobs = jobs.filter(business__area__id=area_param)

        if position_param is not None:
            jobs = jobs.filter(position_type=position_param)

        return jobs


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CreateJobApplicationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer


class CreateBusinessView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CreateBusinessSerializer

    def get_queryset(self):
        return Business.objects.filter(owners=self.request.user)

    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GetCertificateView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
