from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, CommandParser

from api.factories.utils import joblistings


class Command(BaseCommand):
    help = "Populate Categories based on a csv file"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-a",
            "--categories_file",
            help="path to an appropriate csv file to load (default: %(default)s)",
            type=Path,
            default=settings.API_FACTORY_PATHS["categories"],
        )

    def handle(self, *args, **options):
        categories_file = options["categories_file"]

        if categories_file is None or not categories_file.exists():
            raise CommandError(f"Import file {categories_file} does not exist")
        cats = joblistings.JobListingsManager.populate_categories(categories_file)

        self.stdout.write(self.style.SUCCESS(f"Created {len(cats)} categories."))
