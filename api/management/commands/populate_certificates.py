from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, CommandParser

from api.factories.utils import joblistings


class Command(BaseCommand):
    help = "Populate Certificates based on a csv file"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-a",
            "--certificates_file",
            help="path to an appropriate csv file to load (default: %(default)s)",
            type=Path,
            default=settings.API_FACTORY_PATHS["certificates"],
        )

    def handle(self, *args, **options):
        certificates_file = options["certificates_file"]

        if certificates_file is None or not certificates_file.exists():
            raise CommandError(f"Import file {certificates_file} does not exist")
        certs = joblistings.JobListingsManager.populate_certificates(certificates_file)

        self.stdout.write(self.style.SUCCESS(f"Created {len(certs)} certificates."))
