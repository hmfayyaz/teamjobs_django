# Generated by Django 4.2.1 on 2023-06-12 11:31

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0024_alter_jobapplication_last_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jobapplication",
            name="cv",
            field=models.FileField(
                blank=True,
                storage=api.models.get_cv_storage,
                upload_to=api.models.cv_upload_to,
                verbose_name="cv",
            ),
        ),
    ]