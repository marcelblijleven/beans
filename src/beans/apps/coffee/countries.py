from typing import Optional

from django.conf import settings

from django_countries.fields import Countries, Country


class OriginCountries(Countries):
    only = settings.COUNTRIES_FILTER


def get_country(code: str) -> Optional[Country]:
    country = Country(code)

    if not country.name:
        return None

    return Country(code)


def get_country_by_name(name: str) -> Optional[Country]:
    if (code := Countries().by_name(name)) == "":
        return None

    return get_country(code)
