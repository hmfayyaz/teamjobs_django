# Generated by Django 4.1.6 on 2023-02-11 21:52

import address.models
import django.db.models.deletion
import django_quill.fields
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("address", "0003_auto_20200830_1851"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Area",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=254)),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("ACT", "Australian Capital Territory"),
                            ("NSW", "New South Wales"),
                            ("NT", "Northern Territory"),
                            ("QLD", "Queensland"),
                            ("SA", "South Australia"),
                            ("TAS", "Tasmania"),
                            ("VIC", "Victoria"),
                            ("WA", "Western Australia"),
                        ],
                        max_length=3,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Business",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=254)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, region=None
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                (
                    "address",
                    address.models.AddressField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="address.address",
                    ),
                ),
                (
                    "area",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="api.area"
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "owners",
                    models.ManyToManyField(
                        related_name="businesses", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=254)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Certificate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=254)),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("ACT", "Australian Capital Territory"),
                            ("NSW", "New South Wales"),
                            ("NT", "Northern Territory"),
                            ("QLD", "Queensland"),
                            ("SA", "South Australia"),
                            ("TAS", "Tasmania"),
                            ("VIC", "Victoria"),
                            ("WA", "Western Australia"),
                        ],
                        max_length=3,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JobListing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", django_quill.fields.QuillField()),
                ("listing_expiry", models.DateTimeField()),
                (
                    "business",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="api.business"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="api.category"
                    ),
                ),
                (
                    "certificates_required",
                    models.ManyToManyField(
                        related_name="joblistings", to="api.certificate"
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name="JobApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=254)),
                ("last_name", models.CharField(max_length=254)),
                (
                    "mobile",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, region=None
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("experience", models.TextField()),
                ("cv", models.FileField(upload_to="uploads/")),
                (
                    "job_listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="api.joblisting"
                    ),
                ),
            ],
        ),
    ]