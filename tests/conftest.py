import os

import factory.random
import pytest
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest

from beans.apps.base.models import User
from beans.apps.coffee.models import TastingNote


@pytest.fixture(scope="session", autouse=True)
def set_faker_seed():
    factory.random.reseed_random("beans.application")


@pytest.fixture(scope="session", autouse=True)
def set_django_secret():
    os.environ["DJANGO_SECRET_KEY"] = "t0ps3cr3t-key"


@pytest.fixture()
def logged_in_user() -> User:
    user, created = User.objects.get_or_create(email="testuser@mail.com")

    return user


@pytest.fixture()
def anonymous_user() -> AnonymousUser:
    user = AnonymousUser()
    return user


@pytest.fixture()
def request_with_anonymous_user(rf, anonymous_user) -> HttpRequest:
    request = rf.request()
    request.user = anonymous_user
    return request


@pytest.fixture()
def user_with_one_coffee(db, django_user_model) -> User:
    user = django_user_model.objects.create(email="test@email.com")
    processing = user.processing_set.create(name="Natural")
    roaster = user.roaster_set.create(name="La Cabra")

    coffee = user.coffee_set.create(
        name="Coffee",
        country="Ethiopia",
        processing=processing,
        roaster=roaster,
        roasting_date="2022-03-23",
        rating=4,
    )

    coffee.tasting_notes.add(
        TastingNote.objects.create(user=user, name="Dark chocolate"),
        TastingNote.objects.create(user=user, name="Floral"),
    )

    coffee.save()

    return user


@pytest.fixture()
def secondary_user_with_one_coffee(db, django_user_model) -> User:
    user = django_user_model.objects.create(email="secondary_test@email.com")
    processing = user.processing_set.create(name="Natural")
    roaster = user.roaster_set.create(name="La Cabra")

    coffee = user.coffee_set.create(
        name="Coffee",
        country="Ethiopia",
        processing=processing,
        roaster=roaster,
        roasting_date="2022-03-23",
        rating=4,
    )

    coffee.tasting_notes.add(
        TastingNote.objects.create(user=user, name="Dark chocolate"),
        TastingNote.objects.create(user=user, name="Floral"),
    )

    coffee.save()

    return user
