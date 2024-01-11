# Generated by Django 4.1.7 on 2023-03-15 00:20

from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0011_alter_jobapplication_cv"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="area",
            options={"ordering": ["state", "name"]},
        ),
        migrations.AlterModelOptions(
            name="business",
            options={"ordering": ["name", "area__name"]},
        ),
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ["name"], "verbose_name_plural": "categories"},
        ),
        migrations.AlterModelOptions(
            name="certificate",
            options={"ordering": ["state", "name"]},
        ),
        migrations.AlterModelOptions(
            name="joblisting",
            options={"ordering": ["-listing_created"]},
        ),
        migrations.AddIndex(
            model_name="business",
            index=models.Index(
                models.OrderBy(django.db.models.functions.text.Upper("name")),
                name="business_upper_name_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="joblisting",
            index=models.Index(
                fields=["-listing_created"], name="api_joblist_listing_ea75d2_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="joblisting",
            index=models.Index(
                fields=["listing_expiry"], name="api_joblist_listing_41d533_idx"
            ),
        ),
    ]
