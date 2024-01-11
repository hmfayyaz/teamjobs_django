import csv
import itertools

import pytest
from address import models as am
from django.conf import settings as django_settings

from api.factories.utils import areas


def area_csv(n=None):
    csv_path = django_settings.API_FACTORY_PATHS["areas"]
    return itertools.islice(
        csv.DictReader(csv_path.open(encoding="utf8", newline="")), 0, n
    )


@pytest.fixture
def area_manager():
    return areas.AreaManager()


@pytest.fixture(params=area_csv(10))
def address_with_pc_and_area(request, db):
    item = request.param
    address = {
        "suburb": item["locality"],
        "country": "Australia",
        "postal_code": item["postcode"],
    }
    yield address, {"name": item["tr"], "state": item["state"]}


@pytest.fixture(params=area_csv(10))
def address_with_state_and_area(request, db):
    item = request.param
    address = {
        "suburb": item["locality"],
        "state": item["state"],
        "country": "Australia",
    }
    yield address, {"name": item["tr"], "state": item["state"]}


def test_area_manager_load_csv_file_settings(area_manager):
    area_manager.load_csv_file()
    assert areas.area_manager._setup
    assert len(area_manager.areas) == 2


def test_area_manager_load_csv_file_path(area_manager, settings):
    area_manager.load_csv_file(settings.API_FACTORY_PATHS["areas"])
    assert area_manager._setup
    assert len(area_manager.lookup_pc_loc) == 43
    assert len(area_manager.lookup_pc_loc["4573"]) == 6


def test_area_manager_load_csv_file_path_string(area_manager, settings):
    area_manager.load_csv_file(str(settings.API_FACTORY_PATHS["areas"]))
    assert area_manager._setup
    assert len(area_manager.lookup_pc_loc) == 43
    assert len(area_manager.lookup_pc_loc["4573"]) == 6


def test_area_manager_load_csv_areas(area_manager):
    area_manager.load_csv_file()
    assert len(area_manager.areas) == 2


def test_area_manager_load_csv_lookup_pc_loc(area_manager, settings):
    area_manager.load_csv_file()
    assert len(area_manager.lookup_pc_loc) == 43
    assert len(area_manager.lookup_pc_loc["4573"]) == 6


def test_area_manager_load_csv_not_exist(area_manager):
    with pytest.raises(ValueError):
        area_manager.load_csv_file("doesnotexist.csv")


@pytest.mark.django_db
def test_area_manager_populate_areas_noload(area_manager):
    objs, n = area_manager.populate_areas()
    assert len(objs) == n


@pytest.mark.django_db
def test_area_manager_populate_areas(area_manager):
    area_manager.load_csv_file()
    objs, n = area_manager.populate_areas()
    assert len(objs) == n


@pytest.mark.django_db
def test_area_manager_find_area_for_address_pc_loc(
    address_with_pc_and_area, area_manager
):
    assert address_with_pc_and_area[1] == area_manager.find_area_for_address(
        address_with_pc_and_area[0]
    )


def test_area_manager_find_area_for_address_state_loc(
    address_with_state_and_area, area_manager
):
    assert address_with_state_and_area[1] == area_manager.find_area_for_address(
        address_with_state_and_area[0]
    )


def test_area_manager_find_area_for_address_invalid_arg(area_manager):
    with pytest.raises(ValueError):
        area_manager.find_area_for_address([1, 2])
