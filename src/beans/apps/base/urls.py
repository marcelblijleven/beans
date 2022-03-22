from django.urls import path

from beans.apps.base.views import home_view

urlpatterns = [
    path("", home_view, name="home")
]
