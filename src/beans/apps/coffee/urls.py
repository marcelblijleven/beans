from django.urls import path

from beans.apps.coffee.views import (
    add_coffee_view,
    coffee_detail_view,
    coffee_list_view,
    delete_coffee_view,
    roaster_list_view,
    add_roaster_view,
)

urlpatterns = [
    path("", coffee_list_view, name="coffee-list"),
    path("<int:pk>", coffee_detail_view, name="coffee-detail"),
    path("<int:pk>/delete", delete_coffee_view, name="coffee-delete"),
    path("add/", add_coffee_view, name="add-coffee"),
    path("roasters/", roaster_list_view, name="roaster-list"),
    path("roasters/add", add_roaster_view, name="add-roaster"),
]
