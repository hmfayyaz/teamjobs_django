import csv
import pathlib
from pathlib import Path

from django.conf import settings
from django.utils.functional import SimpleLazyObject

from api import models

AreaItem = dict[str, str]
LookupDictT = dict[str, dict[str, AreaItem]]


class AreaManager:
    def __init__(self) -> None:
        self.lookup_pc_loc: LookupDictT = {}
        self.lookup_state_loc: LookupDictT = {}
        self.areas: dict[str, dict[str, str]] = {}
        self._setup: bool = False

    def lookup_area_postcode_locality(self, postcode, locality):
        return self.lookup_pc_loc.get(postcode, {}).get(locality, {})

    def lookup_area_state_locality(self, state, locality):
        return self.lookup_state_loc.get(state, {}).get(locality, {})

    def load_csv_file(self, area_file: str | Path | None = None) -> None:
        if area_file is None:
            area_file = settings.API_FACTORY_PATHS["areas"]
        if isinstance(area_file, str):
            area_file = pathlib.Path(area_file)
        if not area_file.exists():
            raise ValueError(f"{area_file!s} does not exist")
        for item in csv.DictReader(area_file.open()):
            area_item = {"name": item["tr"], "state": item["state"]}
            self.areas[f"{area_item['name']}-{area_item['state']}"] = area_item
            self.lookup_pc_loc.setdefault(
                item["postcode"], {item["locality"]: area_item}
            ).setdefault(item["locality"], area_item)
            self.lookup_state_loc.setdefault(
                item["state"], {item["locality"]: area_item}
            ).setdefault(item["locality"], area_item)
        self._setup = True

    def find_area_for_address(self, address: dict) -> dict[str, str]:
        if not self._setup:
            self.load_csv_file()
        if not isinstance(address, dict):
            raise ValueError("Must provide address as a dict, not a %s" % type(address))
        postal_code = address.get("postal_code", "")
        locality = address.get("suburb", "")
        state = address.get("state", "")
        if area := self.lookup_area_postcode_locality(postal_code, locality):
            return area
        if area := self.lookup_area_state_locality(state, locality):
            return area
        return {}

    def populate_areas(self) -> tuple[list[models.Area], int]:
        if not self._setup:
            self.load_csv_file()
        results = [
            models.Area.objects.get_or_create(defaults=None, **instance)
            for instance in self.areas.values()
        ]
        num_created: int = sum([x[1] for x in results])
        area_objects: list[models.Area] = [x[0] for x in results]
        return area_objects, num_created


area_manager = SimpleLazyObject(AreaManager)
