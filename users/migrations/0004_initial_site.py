from django.db import migrations
from django.conf import settings


def add_initial_site(apps, _):
    site_klass = apps.get_model("sites", "Site")
    initial_site = site_klass(
        id=settings.SITE_ID, domain=settings.DOMAIN_NAME, name=settings.DOMAIN_NAME
    )
    initial_site.save()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_teamuser_options_and_more"),
        ("sites", "0002_alter_domain_unique"),
    ]
    operations = [
        migrations.RunPython(add_initial_site, reverse_code=migrations.RunPython.noop)
    ]
