# Generated by Django 4.1.7 on 2023-02-26 12:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0005_alter_joblisting_business"),
    ]

    operations = [
        migrations.AlterField(
            model_name="joblisting",
            name="title",
            field=models.CharField(max_length=254, verbose_name="job title"),
        ),
        migrations.AddConstraint(
            model_name="area",
            constraint=models.UniqueConstraint(
                fields=("name", "state"), name="api_area_unique_name_state"
            ),
        ),
    ]
