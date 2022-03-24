from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from beans.apps.base.forms import RegistrationForm
from beans.apps.base.utils import get_aggregated_results


def home_view(request: HttpRequest) -> HttpResponse:
    context = {
        "page": "home",
        "aggregated_results": {}
    }

    if request.user.is_authenticated:
        user = request.user
        context["aggregated_results"] = get_aggregated_results(user)

    return render(request, "home.html", context=context)


def login_view(request: HttpRequest) -> HttpResponse:
    context = {
        "page": "login"
    }

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        # TODO: add rate limiting
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        if (user := authenticate(request, email=email, password=password)) is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password incorrect")
            return render(request, "login_register.html", context=context)

    return render(request, "login_register.html", context=context)


@login_required(login_url="/login")
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")


def register_view(request: HttpRequest) -> HttpResponse:
    form = RegistrationForm()
    context = {
        "page": "register",
        "form": form,
    }

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=True)
            login(request, user)
            return redirect("home")
        else:
            context["form"] = form
            return render(request, "login_register.html", context=context)

    return render(request, "login_register.html", context=context)
