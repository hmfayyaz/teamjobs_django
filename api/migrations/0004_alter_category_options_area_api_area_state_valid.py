# Generated by Django 4.1.7 on 2023-02-23 13:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_joblisting_listing_created"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "categories"},
        ),
        migrations.AddConstraint(
            model_name="area",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("state__in", ["ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"])
                ),
                name="api_area_state_valid",
            ),
        ),
    ]