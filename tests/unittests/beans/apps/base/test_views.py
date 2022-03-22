from pytest_mock import MockFixture

from beans.apps.base.views import home_view


def test_home_view(rf, mocker: MockFixture):
    mock_render = mocker.patch("beans.apps.base.views.render")
    request = rf.request()

    home_view(request)
    mock_render.assert_called_with(request, "home.html", context={})
