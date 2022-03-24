from django_countries.fields import Country

from beans.apps.coffee.countries import OriginCountries, get_country_by_name, get_country


def test_get_country():
    assert get_country("XX") is None
    assert get_country("NL") == Country(code="NL")


def test_get_country_by_name():
    assert get_country_by_name("i do not exist") is None
    assert get_country_by_name("Netherlands") == Country(code="NL")


def test_origin_countries(settings):
    origin_countries = OriginCountries()
    settings_countries = settings.COUNTRIES_FILTER + ["UN"]
    countries = [key for key in origin_countries.countries.keys()]

    assert countries == settings_countries
