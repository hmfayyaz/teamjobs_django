# Generated by Django 4.1.7 on 2023-03-28 17:37

from localflavor.au.au_states import STATE_CHOICES
from django.db import migrations

STATE_LOOKUP = dict(STATE_CHOICES)


def json_to_addressfield(address):
    address = {k: v.upper() for k, v in address.items()}
    street_parts = address["line_1"].split()
    seen_digit = False
    route = street_number = None
    for idx, part in enumerate(street_parts):
        if not seen_digit and part and any(map(str.isdigit, part)):
            seen_digit = True
            continue
        if part and part[0].isalpha():
            route = " ".join(street_parts[idx:])
            street_number = " ".join(street_parts[:idx])
            break
    if route is None:
        route = address["line1"]
        if address["line2"]:
            street_number = address["line2"]
    address_parts = [
        address["line_1"],
        f"{address['suburb']} {address['state']} {address['postal_code']}",
        address["country"],
    ]
    if "line_2" in address:
        address_parts.insert(0, address["line_2"])

    return {
        "raw": ", ".join(address_parts),
        "formatted": ", ".join(address_parts),
        "street_number": street_number,
        "route": route,
        "country": address["country"],
        "state": STATE_LOOKUP.get(address["state"], address["state"]).upper(),
        "locality": address["suburb"],
        "postal_code": address["postal_code"],
    }


def addressfield_to_json(address_old):
    json_field_dict = {
        "line_1": f"{address_old.street_number} {address_old.route}",
    }
    if address_old.locality is not None:
        loc = address_old.locality
        json_field_dict["suburb"] = loc.name
        json_field_dict["postal_code"] = loc.postal_code
        if loc.state is not None:
            if loc.state.code is not None:
                json_field_dict["state"] = loc.state.code
            elif loc.state.name is not None:
                json_field_dict["state"] = loc.state.name
            if loc.state.country is not None:
                if loc.state.country.name is not None:
                    json_field_dict["country"] = loc.state.country.name
                elif loc.state.country.code is not None:
                    json_field_dict["country"] = loc.state.country.code
    if address_old.raw is not None:
        json_field_dict["raw"] = address_old.raw
    if address_old.longitude is not None:
        json_field_dict["location"] = {
            "longitude": address_old.longitude,
            "latitude": address_old.latitude,
        }
    return json_field_dict


def convert_addresses_to_json(apps, schema_editor):
    business_model = apps.get_model("api", "Business")
    businesses = business_model.objects.all()
    for business in businesses:
        business.address = addressfield_to_json(business.address_old)
    businesses.bulk_update(businesses, ["address"])


def convert_json_to_addresses(apps, schema_editor):
    business_model = apps.get_model("api", "Business")

    businesses = business_model.objects.all()
    for business in businesses:
        business.address_old = json_to_addressfield(business.address)
    businesses.bulk_update(businesses, ["address_old"])


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0015_business_address"),
    ]

    operations = [
        migrations.RunPython(
            convert_addresses_to_json, reverse_code=convert_json_to_addresses
        ),
    ]