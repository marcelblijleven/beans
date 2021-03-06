from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, redirect
from django_countries.fields import Country

from beans.apps.base.models import User
from beans.apps.coffee.exceptions import CoffeeException
from beans.apps.coffee.forms import AddCoffeeForm, AddRoasterForm
from beans.apps.coffee.countries import OriginCountries
from beans.apps.coffee.models import Coffee


def process_add_coffee_form(form: AddCoffeeForm, user: User):
    if not form.is_valid():
        raise CoffeeException("expected form to be valid")

    cd = form.cleaned_data
    name = cd.get("name")
    country = cd.get("country")
    processing_name = cd.get("processing")
    roaster_name = cd.get("roaster")
    roasting_date = cd.get("roasting_date")
    rating = cd.get("rating")

    processing, _ = user.processing_set.get_or_create(name=processing_name)
    roaster, _ = user.roaster_set.get_or_create(name=roaster_name)

    user.coffee_set.create(
        name=name,
        country=country,
        processing=processing,
        roaster=roaster,
        roasting_date=roasting_date,
        rating=rating,
    )


@login_required(login_url="/login")
def coffee_list_view(request: HttpRequest) -> HttpResponse:
    if (query := request.GET.get("q", None)) is not None:
        query = query
        coffee_list = request.user.coffee_set.filter(
            Q(name__icontains=query)
            | Q(country__icontains=query)
            | Q(processing__name__icontains=query)
            | Q(roaster__name__icontains=query)
        ).order_by("-roasting_date", "name")
    else:
        coffee_list = request.user.coffee_set.all().order_by("-roasting_date", "name")

    context = {
        "page": "coffee-list",
        "query": query,
        "coffee_list": coffee_list,
    }

    return render(request, "coffees.html", context=context)


@login_required(login_url="/login")
def add_coffee_view(request: HttpRequest) -> HttpResponse:
    countries = [Country(code=country[0]) for country in OriginCountries()]
    processing = request.user.processing_set.all().order_by("name")
    roasters = request.user.roaster_set.all().order_by("name")

    context = {
        "page": "add-coffee",
        "countries": countries,
        "existing_processing": processing,
        "existing_roasters": roasters,
    }

    if request.method == "POST":
        form = AddCoffeeForm(request.POST)

        if form.is_valid():
            process_add_coffee_form(form, request.user)
            return redirect("coffee-list")
        else:
            messages.error(request, "An error occurred while processing the form")
            # TODO: return errors to frontend

    return render(request, "add_coffee.html", context=context)


@login_required(login_url="/login")
def coffee_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        coffee = request.user.coffee_set.get(id=pk)
    except Coffee.DoesNotExist:
        raise Http404("Coffee does not exist or you do not have permission to view it")

    context = {
        "page": "coffee-detail-page",
        "coffee": coffee,
        "rating_range": range(coffee.rating or 0),
        "information": get_detail_information(coffee),
    }

    return render(request, "coffee_detail.html", context=context)


@login_required(login_url="/login")
def roaster_list_view(request: HttpRequest) -> HttpResponse:
    roaster_list = request.user.roaster_set.all().annotate(count=Count("coffee")).order_by("-count", "name")
    context = {
        "page": "roaster-list",
        "roaster_list": roaster_list,
    }

    return render(request, "roasters.html", context=context)


@login_required(login_url="/login")
def add_roaster_view(request: HttpRequest) -> HttpResponse:
    context = {"page": "add-roaster", "form": AddRoasterForm()}

    if request.method == "POST":
        form = AddRoasterForm(request.POST)
        context["form"] = form

        if form.is_valid():
            roaster = form.save(commit=False)
            roaster.user = request.user
            roaster.save()
            return redirect("roaster-list")
        else:
            messages.error(request, "An error occurred while processing the form")
            # TODO: return errors to frontend

    return render(request, "add_roaster.html", context=context)


@login_required()
def delete_coffee_view(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        coffee = Coffee.objects.get(id=pk)
        coffee.delete()
        messages.info(request, f"Successfully deleted {coffee.name}")

    except Coffee.DoesNotExist:
        messages.info(request, "Could not delete coffee because it doesn't exists")

    return redirect("/coffees")


def get_detail_information(coffee: Coffee) -> dict[str, str]:
    return {
        "Country": coffee.country,
        "Processing": coffee.processing.name,
        "Tasting notes": coffee.tasting_notes_list,
    }
