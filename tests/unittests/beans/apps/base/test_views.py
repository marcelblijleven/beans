import pytest
from django.shortcuts import render
from pytest_mock import MockFixture

from beans.apps.base.forms import RegistrationForm
from beans.apps.base.views import home_view, login_view, logout_view, register_view


def test_home_view(request_with_anonymous_user, mocker: MockFixture):
    mock_render = mocker.patch("beans.apps.base.views.render", wraps=render)
    home_view(request_with_anonymous_user)
    expected_context = {
        "page": "home",
    }
    mock_render.assert_called_with(request_with_anonymous_user, "home.html", context=expected_context)


def test_home_view_logged_in_user(rf, user_with_one_coffee, mocker: MockFixture):
    mock_render = mocker.patch("beans.apps.base.views.render", wraps=render)
    request = rf.request()
    request.user = user_with_one_coffee

    home_view(request)

    expected_context = {
        "page": "home",
    }

    mock_render.assert_called_with(request, "home.html", context=expected_context)


def test_login_view(request_with_anonymous_user, mocker: MockFixture):
    mock_render = mocker.patch("beans.apps.base.views.render")

    login_view(request_with_anonymous_user)

    expected_context = {"page": "login"}
    mock_render.assert_called_with(request_with_anonymous_user, "login_register.html", context=expected_context)


@pytest.mark.django_db
def test_login_view_post_form(rf, anonymous_user, mocker: MockFixture, django_user_model):
    email = "test@email.com"
    password = "tops3cret"
    user = django_user_model.objects.create(email=email, password=password)
    mock_redirect = mocker.patch("beans.apps.base.views.redirect")
    mock_authenticate = mocker.patch("beans.apps.base.views.authenticate", return_value=user)
    mock_login = mocker.patch("beans.apps.base.views.login")

    request = rf.post("/login", data={"email": email, "password": password})
    request.user = anonymous_user

    login_view(request)

    mock_authenticate.assert_called_with(request, email=email, password=password)
    mock_login.assert_called_with(request, user)
    mock_redirect.assert_called_with("home")


@pytest.mark.django_db
def test_login_view_post_form_invalid_user(rf, anonymous_user, mocker: MockFixture, django_user_model):
    email = "test@email.com"
    password = "tops3cret"
    mock_render = mocker.patch("beans.apps.base.views.render")
    mock_authenticate = mocker.patch("beans.apps.base.views.authenticate", return_value=None)
    mock_messages = mocker.patch("beans.apps.base.views.messages")

    request = rf.post("/login", data={"email": email, "password": password})
    request.user = anonymous_user

    login_view(request)

    mock_authenticate.assert_called_with(request, email=email, password=password)
    mock_render.assert_called_with(request, "login_register.html", context={"page": "login"})
    mock_messages.error.assert_called_with(request, "Username or password incorrect")


@pytest.mark.django_db
def test_login_view_already_authenticated(rf, mocker: MockFixture, logged_in_user):
    mock_redirect = mocker.patch("beans.apps.base.views.redirect")
    request = rf.request()
    request.user = logged_in_user

    login_view(request)

    mock_redirect.assert_called_with("home")


def test_logout_view(rf, client, django_user_model, mocker: MockFixture):
    mock_redirect = mocker.patch("beans.apps.base.views.redirect")
    mock_logout = mocker.patch("beans.apps.base.views.logout")

    request = rf.request()
    user = django_user_model.objects.create(email="test@email.com", password="test")
    request.user = user
    client.login(email="test@email.com", password="test")

    logout_view(request)

    mock_redirect.assert_called_with("home")
    mock_logout.assert_called_with(request)


def test_register_view(request_with_anonymous_user, mocker: MockFixture):
    form = RegistrationForm()
    mock_render = mocker.patch("beans.apps.base.views.render")
    mock_registration_form = mocker.patch("beans.apps.base.views.RegistrationForm", return_value=form)

    register_view(request_with_anonymous_user)

    expected_context = {
        "page": "register",
        "form": form,
    }

    mock_registration_form.assert_called_once()
    mock_render.assert_called_with(request_with_anonymous_user, "login_register.html", context=expected_context)


@pytest.mark.django_db
def test_registration_view_post_form(rf, mocker: MockFixture, anonymous_user, django_user_model):
    mock_redirect = mocker.patch("beans.apps.base.views.redirect")
    mock_login = mocker.patch("beans.apps.base.views.login")

    request = rf.post(
        "/register",
        data={
            "email": "test@email.com",
            "password1": "testpassword",
            "password2": "testpassword",
        },
    )

    user = django_user_model.objects.create(
        email="test@email.com",
        password="testpassword",
    )

    form = mocker.MagicMock()
    form.save.return_value = user
    mock_registration_form = mocker.patch("beans.apps.base.views.RegistrationForm", return_value=form)

    register_view(request)

    mock_registration_form.assert_called_with(request.POST)
    form.save.assert_called_with(commit=True)
    mock_redirect.assert_called_with("home")
    mock_login.assert_called_with(request, user)


@pytest.mark.django_db
def test_registration_view_post_form_invalid_form(rf, mocker: MockFixture, anonymous_user, django_user_model):
    mock_render = mocker.patch("beans.apps.base.views.render")
    mock_login = mocker.patch("beans.apps.base.views.login")

    request = rf.post(
        "/register",
        data={
            "email": "test@email.com",
            "password1": "testpassword",
            "password2": "testpassword",
        },
    )

    user = django_user_model.objects.create(
        email="test@email.com",
        password="testpassword",
    )

    form = mocker.MagicMock()
    form.save.return_value = user
    form.is_valid.return_value = False
    mock_registration_form = mocker.patch("beans.apps.base.views.RegistrationForm", return_value=form)

    register_view(request)

    expected_context = {
        "page": "register",
        "form": form,
    }

    mock_registration_form.assert_called_with(request.POST)
    form.save.assert_not_called()
    mock_render.assert_called_with(request, "login_register.html", context=expected_context)
    mock_login.assert_not_called()
