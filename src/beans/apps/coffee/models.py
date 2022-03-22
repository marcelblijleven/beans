from django.db import models
from django.utils.translation import gettext_lazy as _


class OriginCountry(models.Model):
    class Continent(models.TextChoices):
        AFRICA = "AF", _("Africa")
        ANTARCTICA = "AN", _("Antarctica")
        ASIA = "AS", _("Asia")
        OCEANIA = "OC", _("Oceania")
        EUROPE = "EU", _("Europe")
        NORTH_AMERICA = "NA", _("North America")
        SOUTH_AMERICA = "SA", _("South America")

    name = models.CharField(max_length=80, unique=True)
    continent = models.CharField(
        max_length=2,
        choices=Continent.choices
    )
