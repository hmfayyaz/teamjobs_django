# Generated by Django 4.2.1 on 2023-06-12 08:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0023_alter_jobapplication_cv"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jobapplication",
            name="last_name",
            field=models.CharField(max_length=254, verbose_name="last name"),
        ),
    ]