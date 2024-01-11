from django.contrib import admin
from import_export.admin import ExportActionMixin, ExportActionModelAdmin

from .models import Area, Business, Category, Certificate, JobApplication, JobListing


class JobListingAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "listing_created",
        "business",
        "title",
        "area",
        "listing_expiry",
        "status",
    )

    def area(self, obj):
        area = Area.objects.get(id=obj.business.area.id)
        return area


class JobApplicationAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "mobile",
        "email",
        "created",
        "job_title",
        "business",
        "area",
    )

    def job_title(self, obj):
        job = JobListing.objects.get(id=obj.job_listing.id)
        return job.title

    def area(self, obj):
        area = Area.objects.get(id=obj.job_listing.business.area.id)
        return area

    def business(self, obj):
        business = Business.objects.get(id=obj.job_listing.business.id)
        return business.name


# Register your models here.
admin.site.register(Area, ExportActionModelAdmin)
admin.site.register(Business, ExportActionModelAdmin)
admin.site.register(Certificate, ExportActionModelAdmin)
admin.site.register(Category, ExportActionModelAdmin)
admin.site.register(JobListing, JobListingAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
