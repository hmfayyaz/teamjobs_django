from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, CommandParser

from api.factories.utils import areas


class Command(BaseCommand):
    help = "Populate Areas based on a csv file"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-a",
            "--area_file",
            help="path to an appropriate csv file to load (default: %(default)s)",
            type=Path,
            default=settings.API_FACTORY_PATHS["areas"],
        )

    def handle(self, *args, **options):
        area_file = options["area_file"]

        if area_file is None or not area_file.exists():
            raise CommandError(f"Import file {area_file} does not exist")
        areas.area_manager.load_csv_file(area_file)
        area_objs, num_created = areas.area_manager.populate_areas()
        self.stdout.write(
            self.style.SUCCESS(f"Created {num_created} out of {len(area_objs)} areas.")
        )
