from django.db import models

from beans.apps.base.models import User
from beans.apps.coffee.countries import get_country_by_name
from beans.generic_models import TimeStampedModel


class Processing(TimeStampedModel):
    constraints = [
        models.UniqueConstraint(
            fields=["user", "name"],
            name="unique_processing_constraint"
        )
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)


class Roaster(TimeStampedModel):
    constraints = [
        models.UniqueConstraint(
            fields=["user", "name", "country"],
            name="unique_roaster_constraint"
        )
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=80)
    website = models.URLField(null=True)


class TastingNote(TimeStampedModel):
    constraints = [
        models.UniqueConstraint(
            fields=["user", "name"],
            name="unique_tasting_note_constraint"
        )
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Coffee(TimeStampedModel):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name", "country", "roaster", "roasting_date", "processing"],
                name="unique_bean_roaster_constraint"
            )
        ]

    class Rating(models.IntegerChoices):
        VERY_GOOD = 5
        GOOD = 4
        OK = 3
        BAD = 2
        VERY_BAD = 1

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=80)
    processing = models.ForeignKey(Processing, on_delete=models.SET_NULL, null=True)
    roaster = models.ForeignKey(Roaster, on_delete=models.SET_NULL, null=True)
    roasting_date = models.DateField()
    rating = models.IntegerField(choices=Rating.choices, null=True)
    variety = models.CharField(max_length=200, null=True)
    tasting_notes = models.ManyToManyField(TastingNote)

    @property
    def country_flag(self) -> str:
        if (country := get_country_by_name(self.country)) is None:
            return ""

        return country.unicode_flag

    @property
    def tasting_notes_list(self) -> list[str]:
        if not self.tasting_notes.count():
            return []

        tasting_notes = []

        for note in self.tasting_notes.all():
            tasting_notes.append(note.name)

        return tasting_notes
