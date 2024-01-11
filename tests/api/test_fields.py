import pytest

from tests.testapp.models import HtmlFieldModel


@pytest.mark.django_db
def test_html_field():
    model = HtmlFieldModel.objects.create(html_field="<p>Test</p>")
    model.save()
    assert model.html_field == "<p>Test</p>"


@pytest.mark.django_db
def test_html_field_clean():
    model = HtmlFieldModel.objects.create(html_field="<p>     </p>")
    model.save()
    assert model.html_field == " "


@pytest.mark.django_db
def test_html_field_nonexistant_sanitizer():
    model = HtmlFieldModel.objects.create(
        html_field="",
        html_field_invalid_sanitizier="<title>cleanme</title><h3>Heading</h3>",
    )
    model.save()
    assert model.html_field_invalid_sanitizier == "cleanme<h3>Heading</h3>"


@pytest.mark.django_db
def test_html_field_nondefault_sanitizer():
    model = HtmlFieldModel.objects.create(
        html_field="<h1>heading</h1>", html_field_with_sanitizer="<h1>heading</h1>"
    )
    model.save()
    assert model.html_field_with_sanitizer == "heading"
