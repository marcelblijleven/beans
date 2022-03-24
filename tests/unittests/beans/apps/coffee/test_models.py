import pytest

from datetime import datetime

from django.db import IntegrityError

from beans.apps.coffee.models import Coffee, Roaster, Processing


@pytest.mark.django_db
def test_beans_constraint(logged_in_user):
    roaster = Roaster.objects.create(
        user=logged_in_user,
        name="Specialty Coffee Roasters",
        country="The Netherlands",
    )

    processing = Processing.objects.create(
        user=logged_in_user,
        name="Natural",
    )

    date = datetime.now().date()
    _ = Coffee.objects.create(
        user=logged_in_user,
        name="Yirgacheffe",
        country="Ethiopia",
        processing=processing,
        roaster=roaster,
        roasting_date=date,
        rating=5,
    )

    with pytest.raises(IntegrityError) as exc_info:
        Coffee.objects.create(
            user=logged_in_user,
            name="Yirgacheffe",
            country="Ethiopia",
            processing=processing,
            roaster=roaster,
            roasting_date=date,
            rating=1,
        )

    assert "UNIQUE constraint failed" in str(exc_info.value)
