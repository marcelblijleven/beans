import pytest

from beans.apps.coffee.api.authtoken import EmailFieldObtainAuth
from tests.factories.model_factories import UserFactory


@pytest.mark.skip("data attribute seems to be not working")
def test_obtain_authtoken_post(db, api_rf, settings):
    settings.AUTH_USER_MODEL = "base.user"

    user = UserFactory.create()
    request = api_rf.post(
        "/api/auth",
        {
            "email": user.email,
            "password": user.password,
        },
    )

    obtain_auth = EmailFieldObtainAuth()
    response = obtain_auth.post(request)
    assert response == {}
