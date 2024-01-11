# Generated by Django 4.1.7 on 2023-03-01 09:05

import api.storages
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0010_remove_joblisting_job_type_joblisting_position_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jobapplication",
            name="cv",
            field=models.FileField(
                storage=api.storages.CvFileStorage,
                upload_to=api.storages.cv_upload_to,
                verbose_name="cv",
            ),
        ),
    ]