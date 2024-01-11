from django.db.models import Manager, QuerySet
from django.utils import timezone


class JobListingQuerySet(QuerySet):
    def active(self):
        return self.filter(listing_expiry__gt=timezone.now())

    def inactive(self):
        return self.filter(listing_expiry__lte=timezone.now())

    def for_serialization(self):
        return self.select_related(
            "category",
        ).prefetch_related("certificates_required")


class SelectRelatedManager(Manager):
    def get_queryset(self):
        if hasattr(self.model, "eager_load"):
            eager_load = self.model.eager_load
        else:
            eager_load = []
        return super().get_queryset().select_related(*eager_load)


class JobListingManager(Manager):
    def get_queryset(self) -> JobListingQuerySet:
        return JobListingQuerySet(self.model, using=self._db).select_related(
            "business", "business__area"
        )

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()

    def for_serialization(self):
        return self.get_queryset().for_serialization()
