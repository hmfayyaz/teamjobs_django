# Generated by Django 4.1.7 on 2023-02-23 13:03

import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_teamuser_email_alter_teamuser_phone"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="teamuser",
            options={},
        ),
        migrations.AddConstraint(
            model_name="teamuser",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("email"),
                name="user_email_ci_uniqueness",
            ),
        ),
    ]
