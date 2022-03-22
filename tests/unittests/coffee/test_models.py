import pytest

from datetime import datetime

from django.db import IntegrityError

from beans.apps.coffee.models import Beans, OriginCountry, Roaster, Processing


@pytest.mark.django_db
def test_beans_constraint():
    country = OriginCountry.objects.create(
        name="Ethiopia",
        continent="AF",
    )

    roaster = Roaster.objects.create(
        name="Specialty Coffee Roasters",
        country="NL",
    )

    processing = Processing.objects.create(
        name="Natural",
    )

    date = datetime.now().date()
    _ = Beans.objects.create(
        name="Yirgacheffe",
        country=country,
        processing=processing,
        roaster=roaster,
        roasting_date=date,
        rating=5,
    )

    with pytest.raises(IntegrityError) as exc_info:
        Beans.objects.create(
            name="Yirgacheffe",
            country=country,
            processing=processing,
            roaster=roaster,
            roasting_date=date,
            rating=1,
        )

    assert str(exc_info.value) == "UNIQUE constraint failed: coffee_beans.name, coffee_beans.country_id, coffee_beans.roaster_id, coffee_beans.roasting_date, coffee_beans.processing_id"