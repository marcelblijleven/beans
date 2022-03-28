from beans.apps.coffee.api.authentication import BearerTokenAuthentication


def test_bearer_token_authentication():
    auth = BearerTokenAuthentication()
    assert "Bearer" == auth.keyword
