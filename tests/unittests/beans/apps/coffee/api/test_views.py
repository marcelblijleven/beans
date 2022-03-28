from rest_framework.permissions import AllowAny, IsAuthenticated

from beans.apps.base.models import User
from beans.apps.coffee.api.authentication import BearerTokenAuthentication

from beans.apps.coffee.api.views import (
    AuthenticatedUserView,
    CoffeeListView,
    RoasterListView,
    ProcessingListView,
    PublicStatsView,
    UserStatsView,
)


def test_authenticated_user_view():
    view = AuthenticatedUserView()
    assert view.authentication_classes == [BearerTokenAuthentication]
    assert view.permission_classes == [IsAuthenticated]


def test_coffee_list_view(db, api_rf, setup_one_coffee):
    view = CoffeeListView()
    user = User.objects.first()
    request = api_rf.request()
    request.user = user

    response = view.get(request)
    assert response.content == (
        b'[{"name": "A Coffee", "country": "Lesotho", '
        b'"processing": "Natural", "roaster": "A roaster", '
        b'"roasting_date": "2022-03-23", "rating": 4, "variety": null, "tasting_notes": []}]'
    )


def test_roaster_list_view(db, api_rf, setup_one_coffee):
    view = RoasterListView()
    user = User.objects.first()
    request = api_rf.request()
    request.user = user

    response = view.get(request)
    assert response.content == b'[{"id": 1, "name": "A roaster", "country": "", "website": null, "coffees": 1}]'


def test_processing_list_view(db, api_rf, setup_one_coffee):
    view = ProcessingListView()
    user = User.objects.first()
    request = api_rf.request()
    request.user = user

    response = view.get(request)
    assert response.content == b'[{"id": 1, "name": "Natural", "used": 1}]'


def test_public_stats_view(db, api_rf, setup_one_coffee):
    view = PublicStatsView()

    assert view.permission_classes == [AllowAny]

    user = User.objects.first()
    request = api_rf.request()
    request.user = user

    response = view.get(request)
    assert response.content == (
        b'{"total_coffees": 1, "total_origins": 1, "total_roasters": 1, "top_origins":'
        b' [{"origin": "Lesotho", "count": 1}], "top_roasters": [{"name": "A roaster",'
        b' "count": 1}]}'
    )


def test_user_stats_view(db, api_rf, setup_one_coffee):
    view = UserStatsView()
    user = User.objects.first()
    request = api_rf.request()
    request.user = user

    response = view.get(request)
    assert response.content == (
        b'{"total_coffees": 1, "total_origins": 1, '
        b'"total_roasters": 1, "top_origins": [{"origin": "Lesotho", "count": 1}], '
        b'"top_roasters": [{"name": "A roaster", "count": 1}]}'
    )
