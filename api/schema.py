from localflavor.au.au_states import STATE_CHOICES

ADDRESS_SCHEMA = {
    "title": "address",
    "type": "object",
    "properties": {
        "line_1": {
            "title": "Address line 1",
            "type": "string",
            "placeholder": "Street address, P.O. box, company name, c/o",
            "required": True,
        },
        "line_2": {
            "title": "Address line 2",
            "type": "string",
            "placeholder": "Apartment, suite, unit, building, floor, etc.",
        },
        "suburb": {"title": "Suburb", "type": "string", "required": False},
        "postal_code": {
            "title": "Postcode",
            "type": "string",
            "required": False,
            "minlength": 4,
            "maxlength": 4,
        },
        "state": {
            "title": "State/Territory",
            "type": "string",
            "choices": [s[0] for s in STATE_CHOICES],
            "required": False,
        },
        "country": {
            "type": "string",
            "choices": ["Australia"],
            "default": "Australia",
            "required": True,
        },
        "raw": {
            "type": "string",
            "readonly": True,
        },
        "location": {
            "type": "object",
            "properties": {
                "longitude": {"type": "number", "required": False, "readonly": True},
                "latitude": {"type": "number", "required": False, "readonly": True},
            },
            "required": False,
        },
    },
}
