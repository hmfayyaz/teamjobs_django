# Generated by Django 4.1.7 on 2023-03-29 05:06
import json
from django.db import migrations


def migrate_from_quillfield(apps, schema_editor):
    job_listing = apps.get_model("api", "JobListing")
    for joblisting in job_listing.objects.all():
        joblisting.description_html = joblisting.description.html
        joblisting.save()


def migrate_to_quillfield(apps, schema_editor):
    job_listing = apps.get_model("api", "JobListing")
    for joblisting in job_listing.objects.all():
        quill = {"delta": "", "html": joblisting.description_html}
        joblisting.description.html = json.dumps(quill)
        joblisting.save()


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0019_joblisting_description_html"),
    ]

    operations = [
        migrations.RunPython(
            migrate_from_quillfield, reverse_code=migrate_to_quillfield
        )
    ]