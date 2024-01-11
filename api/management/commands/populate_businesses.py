from pathlib import Path
from typing import Any

import factory
from django.conf import settings
from django.core.management.base import CommandError, CommandParser

from ...factories import BusinessFactory
from ...factories.utils import addresses
from .populate_areas import Command as AreasCommand


class Command(AreasCommand):
    help = "Generate a number of fake businesses"

    def add_arguments(self, parser: CommandParser) -> None:
        super().add_arguments(parser)
        parser.add_argument(
            "-d",
            "--address_csv",
            help="path to a CSV file to populate business addresses from "
            "(default: %(default)s)",
            type=Path,
            default=settings.API_FACTORY_PATHS["addresses"],
        )
        parser.add_argument(
            "-b",
            "--num_businesses",
            help="number of businesses to generate (default: %(default)s)",
            type=int,
            default=100,
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        super().handle(*args, **options)
        address_file = options["address_csv"]
        num_create = options["num_businesses"]
        if address_file is None or not address_file.exists():
            raise CommandError(f"Import file {address_file} does not exist")
        address_mgr = addresses.Addresses()
        address_mgr.load_addresses(address_file)
        businesses = BusinessFactory.create_batch(
            num_create, address=factory.Iterator(address_mgr)
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(businesses)} out of {num_create} requested."
            )
        )
        return None
