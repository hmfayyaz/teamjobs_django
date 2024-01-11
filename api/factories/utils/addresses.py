import csv
import json
from pathlib import Path

from django.conf import settings
from django.utils.functional import SimpleLazyObject


class Addresses:
    def __init__(self):
        self.address_reader: csv.DictReader | None = None
        self._setup = False
        self.address_file = None

    def __iter__(self):
        return self

    def __next__(self):
        if not self._setup:
            self.load_addresses()
        for addr in self.address_reader:
            if "location" in addr and addr["location"]:
                addr["location"] = json.loads(addr["location"].replace("'", '"'))
                for k in addr["location"]:
                    addr["location"][k] = float(addr["location"][k])
            return addr
        raise StopIteration

    def load_addresses(self, address_file: str | Path | None = None) -> None:
        if address_file is None:
            address_path: Path = settings.API_FACTORY_PATHS["addresses"]
        else:
            address_path = Path(address_file)
        if not address_path.exists():
            raise ValueError(f"{address_path!s} does not exist")
        self.address_file = address_path
        self.address_reader = csv.DictReader(
            address_path.open("r", newline="", encoding="utf8")
        )
        self._setup = True


addresses = SimpleLazyObject(Addresses)
