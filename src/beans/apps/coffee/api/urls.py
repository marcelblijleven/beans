from django.urls import path

from beans.apps.coffee.api.authtoken import EmailFieldObtainAuth
from beans.apps.coffee.api.views import RoasterListView, ProcessingListView, CoffeeListView, UserStatsView, PublicStatsView

urlpatterns = [
    path("auth/", EmailFieldObtainAuth.as_view()),
    path("stats/", PublicStatsView.as_view()),
    path("user/coffees/", CoffeeListView.as_view()),
    path("user/roasters/", RoasterListView.as_view()),
    path("user/stats/", UserStatsView.as_view()),
    path("user/processing/", ProcessingListView.as_view()),
]
