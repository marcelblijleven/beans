import datetime

import pytest
from django.http import Http404
from django.shortcuts import render, redirect
from django_countries.fields import Country
from pytest_mock import MockFixture

from beans.apps.coffee.countries import OriginCountries
from beans.apps.coffee.exceptions import CoffeeException
from beans.apps.coffee.forms import AddCoffeeForm, AddRoasterForm
from beans.apps.coffee.views import process_add_coffee_form, coffee_list_view, add_coffee_view, coffee_detail_view, \
    get_detail_information, roaster_list_view, add_roaster_view


@pytest.mark.django_db
def test_process_add_coffee_form(rf, django_user_model):
    user = django_user_model.objects.create(email="test@email.com")
    date = datetime.datetime.now().date()
    request = rf.post("add/", data={
        "name": "Coffee",
        "country": "Ethiopia",
        "processing": "Natural",
        "roaster": "La Cabra",
        "roasting_date": date,
        "rating": 0
    })

    form = AddCoffeeForm(request.POST)

    assert user.coffee_set.count() == 0
    assert user.processing_set.count() == 0
    assert user.roaster_set.count() == 0

    process_add_coffee_form(form, user)

    assert user.coffee_set.count() == 1
    assert user.processing_set.count() == 1
    assert user.roaster_set.count() == 1


@pytest.mark.django_db
def test_process_add_coffee_form_invalid(rf, django_user_model):
    user = django_user_model.objects.create(email="test@email.com")
    date = datetime.datetime.now().date()
    request = rf.post("add/", data={
        "name": "Coffee",
        "country": "Ethiopia",
        "processing": "Natural",
        "roasting_date": date,
        "rating": 0
    })

    form = AddCoffeeForm(request.POST)

    with pytest.raises(CoffeeException) as exc_info:
        process_add_coffee_form(form, user)

    assert not form.is_valid()
    assert str(exc_info.value) == "coffee exception: expected form to be valid"


@pytest.mark.django_db
def test_coffee_list_view(rf, user_with_one_coffee, mocker: MockFixture):
    mock_render = mocker.patch("beans.apps.coffee.views.render", wraps=render)
    request = rf.request()
    request.user = user_with_one_coffee

    processing = user_with_one_coffee.processing_set.get(name="Natural")
    roaster = user_with_one_coffee.roaster_set.get(name="La Cabra")

    user_with_one_coffee.coffee_set.create(
        name="Coffee 2",
        country="El Salvador",
        processing=processing,
        roaster=roaster,
        roasting_date="2022-03-23",
    )

    coffee_list_view(request)

    assert mock_render.mock_calls[0].args == (request, "coffees.html")

    # Doing it this way to be able to compare the coffee list
    assert mock_render.mock_calls[0].kwargs["context"]["page"] == "coffee-list"
    assert mock_render.mock_calls[0].kwargs["context"]["query"] is None
    assert mock_render.mock_calls[0].kwargs["context"]["coffee_list"].count() == user_with_one_coffee.coffee_set.count()


@pytest.mark.django_db
def test_coffee_list_view_with_query(client, rf, django_user_model, mocker: MockFixture):
    mock_render = mocker.patch("beans.apps.coffee.views.render")
    user = django_user_model.objects.create(email="test@email.com", password="test")
    request = rf.get("/coffees", data={
        "q": "Ethiopia"
    })
    request.user = user

    processing = user.processing_set.create(name="Natural")
    roaster = user.roaster_set.create(name="La Cabra")

    user.coffee_set.create(
        name="Coffee",
        country="Ethiopia",
        processing=processing,
        roaster=roaster,
        roasting_date="2022-03-23",
    )
    user.coffee_set.create(
        name="Coffee 2",
        country="El Salvador",
        processing=processing,
        roaster=roaster,
        roasting_date="2022-03-23",
    )

    coffee_list_view(request)

    assert mock_render.mock_calls[0].args == (request, "coffees.html")

    # Doing it this way to be able to compare the coffee list
    assert mock_render.mock_calls[0].kwargs["context"]["page"] == "coffee-list"
    assert mock_render.mock_calls[0].kwargs["context"]["query"] == "Ethiopia"
    assert mock_render.mock_calls[0].kwargs["context"]["coffee_list"].count() == 1


def test_add_coffee_view(rf, django_user_model, mocker: MockFixture):
    mock_render = mocker.patch("beans.apps.coffee.views.render")
    user = django_user_model.objects.create(email="test@email.com")
    user.processing_set.create(name="Natural")
    user.roaster_set.create(name="La Cabra")

    request = rf.request()
    request.user = user

    add_coffee_view(request)

    mock_render.assert_called_once()
    context = mock_render.mock_calls[0].kwargs.get("context")
    assert context
    assert context["page"] == "add-coffee"
    assert "countries" in context
    assert context["existing_processing"].count() == 1
    assert context["existing_roasters"].count() == 1
    assert mock_render.mock_calls[0].args == (request, "add_coffee.html")


def test_add_coffee_view_post_form(rf, django_user_model, mocker: MockFixture):
    mock_redirect = mocker.patch("beans.apps.coffee.views.redirect")
    user = django_user_model.objects.create(email="test@email.com")
    user.processing_set.create(name="Natural")
    user.roaster_set.create(name="La Cabra")

    assert user.coffee_set.count() == 0

    request = rf.post("/add", data={
        "name": "Finca Santa Rosa",
        "country": "El Salvador",
        "processing": user.processing_set.get(name="Natural"),
        "roaster": user.roaster_set.get(name="La Cabra"),
        "roasting_date": "2022-02-14",
        "rating": 4,
    })

    request.user = user
    form = AddCoffeeForm(request.POST)
    mock_add_coffee_form = mocker.patch("beans.apps.coffee.views.AddCoffeeForm", return_value=form)

    add_coffee_view(request)

    mock_add_coffee_form.assert_called_once_with(request.POST)
    mock_redirect.assert_called_once_with("coffee-list")
    assert user.coffee_set.count() == 1
    assert user.coffee_set.first().name == "Finca Santa Rosa"


def test_add_coffee_view_post_form_invalid(rf, django_user_model, mocker: MockFixture):
    mock_render = mocker.patch("beans.apps.coffee.views.render")
    mock_redirect = mocker.patch("beans.apps.coffee.views.redirect")
    mock_messages = mocker.patch("beans.apps.coffee.views.messages")
    user = django_user_model.objects.create(email="test@email.com")
    user.processing_set.create(name="Natural")
    user.roaster_set.create(name="La Cabra")

    assert user.coffee_set.count() == 0

    request = rf.post("/add", data={})

    request.user = user

    mock_form = mocker.MagicMock()
    mock_form.is_valid.return_value = False
    mock_add_coffee_form = mocker.patch("beans.apps.coffee.views.AddCoffeeForm", return_value=mock_form)

    add_coffee_view(request)

    mock_add_coffee_form.assert_called_once_with(request.POST)
    mock_redirect.assert_not_called()
    mock_messages.error.assert_called_with(request, "An error occurred while processing the form")
    mock_render.assert_called_once()
    assert user.coffee_set.count() == 0


@pytest.mark.django_db
def test_coffee_detail_view(rf, user_with_one_coffee, mocker: MockFixture):
    mock_detail_information = mocker.patch(
        "beans.apps.coffee.views.get_detail_information",
        wraps=get_detail_information,
    )
    mock_render = mocker.patch(
        "beans.apps.coffee.views.render",
        wraps=render,
    )

    request = rf.request()
    request.user = user_with_one_coffee
    coffee = user_with_one_coffee.coffee_set.first()

    coffee_detail_view(request, pk=coffee.pk)

    mock_detail_information.assert_called_once_with(user_with_one_coffee.coffee_set.first())
    mock_render.assert_called_once_with(
        request, "coffee_detail.html", context={
            "page": "coffee-detail-page",
            "coffee": coffee,
            "rating_range": range(4),
            "information": get_detail_information(coffee),
        }
    )


@pytest.mark.django_db
def test_coffee_detail_view_does_not_exist(rf, user_with_one_coffee, mocker: MockFixture):
    mock_detail_information = mocker.patch(
        "beans.apps.coffee.views.get_detail_information",
        wraps=get_detail_information,
    )
    mock_render = mocker.patch(
        "beans.apps.coffee.views.render",
        wraps=render,
    )

    request = rf.request()
    request.user = user_with_one_coffee
    coffee = user_with_one_coffee.coffee_set.first()

    with pytest.raises(Http404) as exc_info:
        coffee_detail_view(request, pk=coffee.pk + 1)

    assert "Coffee does not exist or you do not have permission to view it" == str(exc_info.value)

    mock_detail_information.assert_not_called()
    mock_render.assert_not_called()


@pytest.mark.django_db
def test_coffee_detail_view_does_not_exist_for_user(rf, user_with_one_coffee, secondary_user_with_one_coffee,
                                                    mocker: MockFixture):
    mock_detail_information = mocker.patch(
        "beans.apps.coffee.views.get_detail_information",
        wraps=get_detail_information,
    )
    mock_render = mocker.patch(
        "beans.apps.coffee.views.render",
        wraps=render,
    )

    secondary_user_coffee = secondary_user_with_one_coffee.coffee_set.first()

    request = rf.request()
    request.user = user_with_one_coffee

    with pytest.raises(Http404) as exc_info:
        coffee_detail_view(request, pk=secondary_user_coffee.pk)

    assert "Coffee does not exist or you do not have permission to view it" == str(exc_info.value)

    mock_detail_information.assert_not_called()
    mock_render.assert_not_called()


def test_get_detail_information(db, user_with_one_coffee):
    coffee = user_with_one_coffee.coffee_set.first()
    info = get_detail_information(coffee)
    assert info["Country"] == coffee.country
    assert info["Processing"] == coffee.processing.name
    assert info["Tasting notes"] == ["Dark chocolate", "Floral"]


def test_roaster_list_view(rf, user_with_one_coffee, mocker: MockFixture):
    mock_render = mocker.patch("beans.apps.coffee.views.render", wraps=render)
    request = rf.request()
    request.user = user_with_one_coffee

    roaster_list_view(request)

    mock_render.assert_called_once()
    assert mock_render.mock_calls[0].args == (request, "roasters.html")
    received_context = mock_render.mock_calls[0].kwargs["context"]
    assert received_context["page"] == "roaster-list"
    assert received_context["roaster_list"].count() == 1


def test_add_roaster_view(rf, user_with_one_coffee, mocker: MockFixture):
    mocked_form = mocker.MagicMock()
    mocker.patch("beans.apps.coffee.views.AddRoasterForm", return_value=mocked_form)
    mock_render = mocker.patch("beans.apps.coffee.views.render", wraps=render)

    request = rf.request()
    request.user = user_with_one_coffee

    add_roaster_view(request)

    expected_context = {
        "page": "add-roaster",
        "form": mocked_form,
    }

    mock_render.assert_called_once_with(request, "add_roaster.html", context=expected_context)


def test_add_roaster_view_post_form(db, rf, django_user_model, mocker: MockFixture):
    mock_redirect = mocker.patch("beans.apps.coffee.views.redirect", wraps=redirect)
    mock_render = mocker.patch("beans.apps.coffee.views.render", wraps=render)
    user = django_user_model.objects.create(email="test@email.com")

    assert user.roaster_set.count() == 0

    request = rf.post("/coffee/roasters/add", data={
        "name": "The Roasters",
        "country": "Netherlands",
        "website": "https://test.nl",
    })
    request.user = user

    add_roaster_view(request)

    assert user.roaster_set.count() == 1
    mock_redirect.assert_called_once_with("roaster-list")
    mock_render.assert_not_called()


def test_add_roaster_view_post_form_invalid_form(db, rf, django_user_model, mocker: MockFixture):
    mocked_form = mocker.MagicMock()
    mocked_form.is_valid.return_value = False
    mock_add_roaster_form = mocker.patch("beans.apps.coffee.views.AddRoasterForm", return_value=mocked_form)
    mock_render = mocker.patch("beans.apps.coffee.views.render", wraps=render)
    mock_messages = mocker.patch("beans.apps.coffee.views.messages")
    user = django_user_model.objects.create(email="test@email.com")

    assert user.roaster_set.count() == 0

    request = rf.post("/coffee/roasters/add", data={
        "name": "The Roasters",
        "website": "https://test.nl",
    })
    request.user = user

    add_roaster_view(request)

    assert user.roaster_set.count() == 0
    mock_add_roaster_form.assert_called_with(request.POST)
    mock_messages.error.assert_called_once_with(request, "An error occurred while processing the form")
    mock_render.assert_called_once_with(request, "add_roaster.html", context={
        "form": mocked_form,
        "page": "add-roaster",
    })



