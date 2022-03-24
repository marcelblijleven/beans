from django.urls import path

from beans.apps.coffee.views import add_coffee_view, coffee_detail_view, coffee_list_view

urlpatterns = [
    path("", coffee_list_view, name="coffee-list"),
    path("<int:pk>", coffee_detail_view, name="coffee-detail"),
    path("add-coffee/", add_coffee_view, name="add-coffee"),
]
