from django.core.management.base import BaseCommand, CommandParser

from api.factories.utils import joblistings


class Command(BaseCommand):
    help = "Populate JobListings based on a csv file"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-a",
            "--num_active_listings",
            help="number of active (expires in future) job listings to generate "
            "(default: %(default)s)",
            type=int,
            default=100,
        )
        parser.add_argument(
            "-i",
            "--num_inactive_listings",
            help="number of inactive (expired in the past) job listings to generate "
            "(default: %(default)s)",
            type=int,
            default=50,
        )

    def handle(self, *args, **options):
        active_num = options["num_active_listings"]
        inactive_num = options["num_inactive_listings"]
        listings_act = joblistings.JobListingsManager.populate_active_job_listings(
            active_num
        )
        listings_inact = joblistings.JobListingsManager.populate_inactive_job_listings(
            inactive_num
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(listings_act)} active listings and "
                f"{len(listings_inact)} inactive listings."
            )
        )
