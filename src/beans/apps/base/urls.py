from django.urls import path

from beans.apps.base.views import home_view, login_view, logout_view, register_view

urlpatterns = [
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
]
