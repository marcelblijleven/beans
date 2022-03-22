from django.db import models
from django.utils.translation import gettext_lazy as _

from beans.generic_models import TimeStampedModel


class OriginCountry(TimeStampedModel):
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


class Processing(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True)


class Roaster(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=80)
    website = models.URLField(null=True)


class Beans(TimeStampedModel):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "country", "roaster", "roasting_date", "processing"],
                name="unique_bean_roaster_constraint"
            )
        ]

    class Rating(models.IntegerChoices):
        VERY_GOOD = 5
        GOOD = 4
        OK = 3
        BAD = 2
        VERY_BAD = 1

    name = models.CharField(max_length=200, null=False)
    country = models.ForeignKey(OriginCountry, on_delete=models.SET_NULL, null=True)
    processing = models.ForeignKey(Processing, on_delete=models.SET_NULL, null=True)
    roaster = models.ForeignKey(Roaster, on_delete=models.SET_NULL, null=True)
    roasting_date = models.DateField()
    rating = models.IntegerField(choices=Rating.choices)
