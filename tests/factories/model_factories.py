from factory.django import DjangoModelFactory
from factory.faker import Faker

from beans.apps.base.models import User
from beans.apps.coffee.models import Coffee, Processing, Roaster


class UserFactory(DjangoModelFactory):
    email = Faker("email")

    class Meta:
        model = User


class ProcessingFactory(DjangoModelFactory):
    name = "Natural"

    class Meta:
        model = Processing


class RoasterFactory(DjangoModelFactory):
    name = "A roaster"

    class Meta:
        model = Roaster


class CoffeeFactory(DjangoModelFactory):
    name = "A Coffee"
    country = Faker("country")
    roasting_date = "2022-03-23"
    rating = 4

    class Meta:
        model = Coffee
