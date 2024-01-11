from pathlib import Path

import pytest

from api.factories.utils import addresses


def test_load_addresses_pathlib(settings):
    csv_file = settings.API_FACTORY_PATHS["addresses"]
    addresses.addresses.load_addresses(csv_file)
    assert len(list(addresses.addresses)) == (len(csv_file.open().readlines()) - 1)


def test_load_addresses_pathstr(settings):
    csv_file = settings.API_FACTORY_PATHS["addresses"]
    addresses.addresses.load_addresses(str(csv_file))
    assert len(list(addresses.addresses)) == (len(csv_file.open().readlines()) - 1)


def test_load_addresses_not_exist():
    with pytest.raises(ValueError):
        addresses.addresses.load_addresses("doesnotexist.csv")
