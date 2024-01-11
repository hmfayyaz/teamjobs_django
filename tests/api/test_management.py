import io

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.models import Max

from api.models import Business, JobListing


@pytest.mark.django_db
def test_populate_areas_command():
    out = io.StringIO()
    call_command("populate_areas", stdout=out)
    assert "2 out of 2" in out.getvalue()


def test_populate_areas_command_nofile():
    with pytest.raises(CommandError):
        call_command("populate_areas", "--area_file=doesnotexist.csv")


@pytest.mark.django_db
def test_populate_areas_command_arg(settings):
    out = io.StringIO()
    area_csv = settings.BASE_DIR / "api" / "resources" / "area_locality_postcode.csv"
    call_command("populate_areas", f"--area_file={area_csv!s}", stdout=out)
    assert "77 out of 77" in out.getvalue()


@pytest.mark.slow
@pytest.mark.django_db
def test_populate_businesses_command():
    out = io.StringIO()
    call_command("populate_businesses", stdout=out)
    assert "100 out of 100" in out.getvalue()
    last_id = Business.objects.aggregate(Max("id"))["id__max"]
    b = Business.objects.get(id=last_id)
    assert b.address["suburb"] == "BUNDALL"


@pytest.mark.django_db
def test_populate_businesses_command_size():
    out = io.StringIO()
    call_command("populate_businesses", "--num_businesses=10", stdout=out)
    assert "10 out of 10" in out.getvalue()


@pytest.mark.django_db
def test_populate_businesses_command_address_csv(settings):
    out = io.StringIO()
    err = io.StringIO()
    main_csv = settings.BASE_DIR / "api" / "resources" / "addresses.csv"
    # assert Business.objects.all().count() == 0
    call_command(
        "populate_businesses",
        "--num_businesses=1",
        f"--address_csv={main_csv!s}",
        stdout=out,
        stderr=err,
    )
    last_id = Business.objects.aggregate(Max("id"))["id__max"]
    b = Business.objects.get(id=last_id)
    assert b.address["suburb"] == "VERMONT"


@pytest.mark.django_db
def test_populate_businesses_command_address_csv_dne():
    with pytest.raises(CommandError):
        call_command("populate_businesses", "--address_csv=doesnotexist.csv")


@pytest.mark.django_db
def test_populate_categories_command():
    out = io.StringIO()
    call_command("populate_categories", stdout=out)
    assert "0 categories" in out.getvalue()


@pytest.mark.django_db
def test_populate_categories_command_address_csv_dne():
    with pytest.raises(CommandError):
        call_command("populate_categories", "--categories_file=doesnotexist.csv")


@pytest.mark.django_db
def test_populate_certificates_command():
    out = io.StringIO()
    call_command("populate_certificates", stdout=out)
    assert "0 certificates" in out.getvalue()


@pytest.mark.django_db
def test_populate_certificates_command_address_csv_dne():
    with pytest.raises(CommandError):
        call_command("populate_certificates", "--certificates_file=doesnotexist.csv")


@pytest.mark.slow
@pytest.mark.django_db
def test_populate_job_listings():
    out = io.StringIO()
    JobListing.objects.all().delete()
    assert JobListing.objects.all().count() == 0
    call_command("populate_job_listings", stdout=out)
    assert JobListing.objects.all().count() == 150
    assert JobListing.objects.active().all().count() == 100
    assert JobListing.objects.inactive().all().count() == 50
