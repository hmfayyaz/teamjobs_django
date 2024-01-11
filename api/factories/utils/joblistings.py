import csv
import datetime
from pathlib import Path

from django.conf import settings

from ...models import Category, Certificate, JobListing
from .._factories import JobListingFactory


class JobListingsManager:
    @staticmethod
    def populate_categories(csv_file: str | Path | None = None) -> list[Category]:
        if csv_file is None:
            categories_path = Path(settings.API_FACTORY_PATHS["categories"])
        else:
            categories_path = Path(csv_file)
        reader = csv.DictReader(categories_path.open(encoding="utf8", newline=""))
        created_cats: list[Category] = []
        for cat in reader:
            c, created = Category.objects.get_or_create(
                name=cat["name"], defaults={"description": cat["description"]}
            )
            if created:
                created_cats.append(c)
        return created_cats

    @staticmethod
    def populate_certificates(csv_file: str | Path | None = None) -> list[Category]:
        if csv_file is None:
            certificates_path = Path(settings.API_FACTORY_PATHS["certificates"])
        else:
            certificates_path = Path(csv_file)
        reader = csv.DictReader(certificates_path.open(encoding="utf8", newline=""))
        created_certs: list[Category] = []
        for cert in reader:
            c, created = Certificate.objects.get_or_create(**cert)
            if created:
                created_certs.append(c)
        return created_certs

    @staticmethod
    def populate_active_job_listings(size: int) -> list[JobListing]:
        return JobListingFactory.create_batch(size=size)

    @staticmethod
    def populate_inactive_job_listings(size: int) -> list[JobListing]:
        return JobListingFactory.create_batch(
            size=size,
            listing_expiry=datetime.datetime.now(tz=datetime.UTC)
            - datetime.timedelta(days=4),
        )
