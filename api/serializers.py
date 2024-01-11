from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from localflavor.au.au_states import STATE_CHOICES
from rest_framework import serializers
from rest_framework.utils.field_mapping import get_nested_relation_kwargs
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin

from users.models import TeamUser
from users.serializers import UserSerializer

from .models import Area, Business, Category, Certificate, JobApplication, JobListing

USER_MODEL = get_user_model()


class ModelSerializer(serializers.ModelSerializer, SerializerExtensionsMixin):
    """Model serializer with the extension mixin"""

    def build_nested_field(self, field_name, relation_info, nested_depth):
        """
        Create nested fields for forward and reverse relationships.
        """

        class NestedSerializer(ModelSerializer):
            class Meta:
                model = relation_info.related_model
                depth = nested_depth - 1
                fields = "__all__"

        field_class = NestedSerializer
        field_kwargs = get_nested_relation_kwargs(relation_info)

        return field_class, field_kwargs


class AreaSerializer(ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"


class LatLongSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class FullAddressSerializer(serializers.Serializer):
    line_1 = serializers.CharField()
    line_2 = serializers.CharField(required=False)
    suburb = serializers.CharField(required=False)
    state = serializers.ChoiceField(
        choices=[st[0] for st in STATE_CHOICES], required=False
    )
    country = serializers.CharField(default="Australia")
    location = LatLongSerializer(required=False)
    raw = serializers.CharField(required=False)


class LocationSerializer(serializers.Serializer):
    suburb = serializers.CharField()
    state = serializers.CharField()
    country = serializers.CharField()
    line_1 = serializers.CharField()


class BusinessInJobListingSerializer(ModelSerializer):
    area = AreaSerializer()
    address = LocationSerializer()

    class Meta:
        model = Business
        fields = ["name", "area", "address"]
        depth = 1


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CertificateSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = "__all__"


class OwnerSerializer(UserSerializer):
    class Meta:
        model = TeamUser
        fields = ("id", "email", "first_name", "last_name", "phone")
        read_only_fields = ["email", "date_joined", "last_login"]


class ContactSerializer(UserSerializer):
    class Meta:
        model = TeamUser
        fields = ("id", "email", "first_name", "last_name", "phone")
        read_only_fields = ["email", "date_joined", "last_login"]


class JobListingSerializer(ModelSerializer):
    business = BusinessInJobListingSerializer(read_only=True)
    business_id = serializers.PrimaryKeyRelatedField(
        queryset=Business.objects.all(), source="business", write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    category = CategorySerializer(read_only=True)
    certificates_required = CertificateSerializer(many=True, read_only=True)
    certificates_required_ids = serializers.PrimaryKeyRelatedField(
        queryset=Certificate.objects.all(),
        many=True,
        source="certificates_required",
        write_only=True,
        allow_empty=True,
        required=False,
    )

    class Meta:
        model = JobListing
        fields = "__all__"
        extra_kwargs = {
            "listing_created": {"read_only": True},
        }
        # depth = 1


class CreateBusinessSerializer(ModelSerializer):
    address = FullAddressSerializer()
    area_id = serializers.PrimaryKeyRelatedField(
        queryset=Area.objects.all(), source="area", write_only=True
    )
    area = AreaSerializer(read_only=True)
    owners = OwnerSerializer(many=True, read_only=True)
    owner_ids = serializers.SlugRelatedField(
        queryset=USER_MODEL.objects.all(),
        many=True,
        source="owners",
        slug_field="email",
        write_only=True,
    )
    contact_id = serializers.SlugRelatedField(
        queryset=TeamUser.objects.all(),
        source="contact",
        write_only=True,
        slug_field="email",
    )
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Business
        fields = "__all__"
        extra_kwargs = {"owners": {"allow_empty": True, "required": False}}
        # depth = 1


class JobApplicationSerializer(ModelSerializer):
    job_listing_id = serializers.PrimaryKeyRelatedField(
        queryset=JobListing.objects.all(), source="job_listing", write_only=True
    )
    job_listing = JobListingSerializer(read_only=True)

    class Meta:
        model = JobApplication
        fields = "__all__"
        extra_kwargs = {
            "created": {"read_only": True},
            # Provide path to the file on filesystem, not the url
            "cv": {"use_url": False},
        }

    def create(self, validate_data):
        instance = super(JobApplicationSerializer, self).create(validate_data)

        job = JobListing.objects.get(id=validate_data["job_listing"].id)
        subject = """First Name: {}
Last Name: {}
Mobile: {}
Email: {}
Experience: {}"""
        email = EmailMessage(
            "New Job Application on TeamJob",
            subject.format(
                validate_data["first_name"],
                validate_data["last_name"],
                validate_data["mobile"],
                validate_data["email"],
                validate_data["experience"],
            ),
            "noreply@teamjobs.com.au",
            [job.contact_email],
        )
        if self.data.get("cv") is not None:
            uploaded_file = validate_data["cv"].open("rb")
            email.attach(
                uploaded_file.name, uploaded_file.read(), uploaded_file.content_type
            )
        email.send()
        return instance
