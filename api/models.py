import uuid
from pathlib import PurePath

from django.core.files.storage import storages
from django.db import models
from django.db.models.functions import Upper
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_jsonform.models.fields import JSONField
from localflavor.au.au_states import STATE_CHOICES
from phonenumber_field.modelfields import PhoneNumberField

from users.models import TeamUser

from .fields import CleanHTMLField
from .managers import JobListingManager, SelectRelatedManager
from .schema import ADDRESS_SCHEMA


def cv_upload_to(instance, filename: str) -> str:
    suffix = PurePath(filename).suffix or ""
    return f"job_listing_{instance.job_listing_id}/{uuid.uuid4()}{suffix}"


class Area(models.Model):
    name = models.CharField(_("area name"), max_length=254)
    state = models.CharField(_("state"), max_length=3, choices=STATE_CHOICES)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_state_valid",
                check=models.Q(state__in=[s[0] for s in STATE_CHOICES]),
            ),
            models.UniqueConstraint(
                fields=["name", "state"],
                name="%(app_label)s_%(class)s_unique_name_state",
            ),
        ]
        ordering = ["state", "name"]

    def __repr__(self):
        return f"<Area: id={self.id} name={self.name} state={self.state}>"

    def __str__(self):
        return f"{self.name}, {self.state}"


class Business(models.Model):
    eager_load = ["area"]
    name = models.CharField(_("business name"), max_length=254)
    area = models.ForeignKey(
        Area, on_delete=models.PROTECT, related_name="+", verbose_name=_("area")
    )
    address = JSONField(schema=ADDRESS_SCHEMA, default=dict, verbose_name=_("address"))
    phone = PhoneNumberField(_("phone number"), blank=True)
    email = models.EmailField(_("email"), max_length=254)
    owners = models.ManyToManyField(
        TeamUser,
        related_name="owned_businesses",
        verbose_name=_("owners"),
        help_text=_("Users with administrative access to the business"),
    )
    contact = models.ForeignKey(
        TeamUser,
        on_delete=models.PROTECT,
        verbose_name=_("contact"),
        help_text=_("Primary contact for the business"),
    )

    objects = SelectRelatedManager()

    class Meta:
        indexes = [models.Index(Upper("name").asc(), name="business_upper_name_idx")]
        ordering = ["name", "area__name"]

    def __repr__(self):
        area = self.area.name if self.area_id is not None else ""
        return f"<Business: id={self.id} name={self.name} area={area}>"

    def __str__(self):
        area = self.area.name if self.area_id is not None else ""
        return f"{self.name}, {area}"


class Certificate(models.Model):
    name = models.CharField(_("name"), max_length=254)
    state = models.CharField(_("state"), max_length=3, choices=STATE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "state"],
                name="%(app_label)s_%(class)s_unique_name_state",
            ),
        ]
        ordering = ["state", "name"]

    def __str__(self):
        return f"{self.name} ({self.state})"

    def __repr__(self):
        return f"<Certificate: id={self.id} name={self.name} state={self.state}>"


class Category(models.Model):
    name = models.CharField(_("area name"), max_length=254, unique=True)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        verbose_name_plural = _("categories")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Category: id={self.id} name={self.name}>"


class JobListing(models.Model):
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="job_listings",
        verbose_name=_("business"),
    )
    title = models.CharField(_("job title"), max_length=254)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="job_listings",
        verbose_name=_("category"),
    )
    description = CleanHTMLField(_("description"))
    position_type = models.CharField(
        _("position type"),
        max_length=1,
        default="",
        choices=[
            ("P", "Permanent"),
            ("C", "Casual"),
            ("S", "Shifts"),
            ("", "Unspecified"),
        ],
    )
    certificates_required = models.ManyToManyField(
        Certificate,
        blank=True,
        related_name="joblistings",
        verbose_name=_("certificates required"),
    )
    listing_expiry = models.DateTimeField(_("listing expiry"))
    listing_created = models.DateTimeField(_("listing create at"), auto_now_add=True)
    contact_name = models.CharField(_("contact name"), max_length=254, blank=True)
    contact_email = models.EmailField(_("contact email"), blank=True)
    contact_phone = PhoneNumberField(_("contact phone"), blank=True)

    objects = JobListingManager()

    class Meta:
        indexes = [
            models.Index(fields=["-listing_created"]),
            models.Index(fields=["listing_expiry"]),
        ]
        ordering = ["-listing_created"]

    def __str__(self):
        return f"{self.title} - {self.business!s}"

    def __repr__(self):
        return (
            f"<JobListing: id={self.id} active={self.status} title={self.title} "
            f"business={self.business!r}>"
        )

    @property
    def status(self):
        return self.listing_expiry > timezone.now()


def get_cv_storage():
    return storages["cv"]


class JobApplication(models.Model):
    eager_load = ["job_listing"]

    first_name = models.CharField(_("first name"), max_length=254)
    last_name = models.CharField(_("last name"), max_length=254)
    mobile = PhoneNumberField(_("mobile"), blank=True)
    email = models.EmailField(_("email"), max_length=254)
    experience = models.TextField(_("experience"))
    cv = models.FileField(
        _("cv"), storage=get_cv_storage, upload_to=cv_upload_to, blank=True
    )
    job_listing = models.ForeignKey(
        JobListing,
        on_delete=models.PROTECT,
        related_name="applications",
        verbose_name=_("job listing"),
    )
    created = models.DateTimeField(_("created at"), auto_now_add=True)
    objects = SelectRelatedManager()

    class Meta:
        indexes = [models.Index(fields=["-created"])]
        ordering = ["-created"]

    def __repr__(self):
        return (
            f"<JobApplication: id={self.id} listing_id={self.job_listing_id} "
            f"name='{self.first_name} {self.last_name}'>"
        )

    def __str__(self):
        return (
            f"Application by {self.first_name} {self.last_name} for "
            f"{self.job_listing!s} - "
            f"{self.created.strftime('%c')}"
        )
