# Generated by Django 4.1.7 on 2023-02-26 12:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0006_alter_joblisting_title_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                max_length=254, unique=True, verbose_name="area name"
            ),
        ),
    ]
