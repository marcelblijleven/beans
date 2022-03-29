import csv

from datetime import datetime, date
from io import TextIOWrapper
from typing import Any

# from django.db import IntegrityError

from beans.apps.base.models import User
from beans.apps.coffee.models import Coffee, Processing, Roaster


def get_csv_headers() -> list[str]:
    return [
        "coffee_name",
        "country",
        "processing",
        "roaster",
        "roasting_date",
        "rating",
        "variety",
        "tasting_notes",
    ]


def csv_to_coffees(user: User, file: TextIOWrapper) -> list[Coffee]:
    """
    Create coffee objects from the provided csv file
    """
    csv_reader = csv.DictReader(file, delimiter=";")
    coffees: list[Coffee] = []

    # errors: list[Exception] = []

    for number, row in enumerate(csv_reader):
        coffees.append(parse_row(user, row, number))
        # try:
        #     coffees.append(parse_row(user, row))
        # except IntegrityError as e:
        #     errors.append(e)

    return coffees


def _validate_row_property(row: dict[str, str], row_number: int, property_name: str) -> str:
    """
    Validates the given property name for the provided row.
    Returns the retrieved property value
    If the property value is None or an empty string, it will raise a ValueError
    """
    value = row.get(property_name, None)

    if not value or value == "":
        raise ValueError(f"{property_name} is a required field in row {row_number}")

    return value


def _validate_row_datestr_property(row: dict[str, str], row_number: int, property_name: str) -> str:
    """
    Validates the given property name for the provided row.
    If the property value is None, an empty string or an invalid date format, it will raise a ValueError
    """
    value = _validate_row_property(row, row_number, property_name)

    try:
        parse_roasting_date(value)
    except ValueError as e:
        raise ValueError(f"roasting_date is invalid in row {row_number}") from e

    return value


def parse_row(user: User, row: dict[str, Any], row_number) -> Coffee:
    """
    Parses a DictReader row and creates a coffee object for the provided user
    """

    coffee_name = _validate_row_property(row, row_number, "coffee_name")
    processing_name = _validate_row_property(row, row_number, "processing")
    roaster_name = _validate_row_property(row, row_number, "roaster")
    roasting_date_str = _validate_row_datestr_property(row, row_number, "roasting_date")

    processing, processing_created = Processing.objects.get_or_create(user=user, name=processing_name)
    roaster, roaster_created = Roaster.objects.get_or_create(user=user, name=roaster_name)
    rating = row.get("rating")

    if rating == "":
        rating = None

    coffee, created = Coffee.objects.get_or_create(
        user=user,
        name=coffee_name,
        processing=processing,
        roaster=roaster,
        roasting_date=roasting_date_str,
        rating=rating,
        variety=row.get("variety", None),
    )

    add_tasting_notes_to_coffee(coffee, get_tasting_notes(row.get("tasting_notes", None)))

    return coffee


def parse_roasting_date(roasting_date_str: str) -> date:
    """
    Parses roasting date from the provided date str
    """
    try:
        return datetime.strptime(roasting_date_str, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError("expected date format to be YYYY-MM-DD") from e


def get_tasting_notes(tasting_notes_str: str) -> list[str]:
    """
    Retrieves a list of str from the comma delimited str value
    """
    if not tasting_notes_str:
        return []

    return [note.strip(" ").lower().capitalize() for note in tasting_notes_str.split(",")]


def add_tasting_notes_to_coffee(coffee: Coffee, tasting_notes: list[str]) -> None:
    """
    Creates and adds tasting notes to the provided coffee object

    This doesn't use bulk_create as it only returns a complete object when using Postgresql.
    In other databases, like sqlite, it will not return a primary key which makes it harder to
    add to the ManyToMany field tasting_notes.
    """

    user = coffee.user

    for note in tasting_notes:
        tasting_note, created = user.tastingnote_set.get_or_create(user=user, name=note)
        coffee.tasting_notes.add(tasting_note)

    coffee.save()
