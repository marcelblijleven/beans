import copy
import os
from datetime import datetime

import pytest

from beans.apps.coffee.models import Coffee
from beans.apps.impex.utils import (
    csv_to_coffees,
    add_tasting_notes_to_coffee,
    parse_row,
    parse_roasting_date,
    get_tasting_notes,
    get_csv_headers,
)
from tests.factories.model_factories import UserFactory


DUMMY_ROW = {
    "coffee_name": "Good coffee",
    "country": "El Salvador",
    "processing": "Natural",
    "roaster": "La Cabra",
    "roasting_date": "2022-03-23",
    "rating": 4,
    "variety": "Pacamara",
    "tasting_notes": "Fruity, Rich,Milk chocolate",
}


def test_get_csv_headers():
    assert [
        "coffee_name",
        "country",
        "processing",
        "roaster",
        "roasting_date",
        "rating",
        "variety",
        "tasting_notes",
    ] == get_csv_headers()


def test_csv_to_coffees(db, test_data_dir):
    user = UserFactory.create()
    assert user.coffee_set.count() == 0
    file_path = os.path.join(test_data_dir, "csv_example.csv")

    with open(file_path) as csv_file:
        csv_to_coffees(user, csv_file)  # noqa

    assert user.coffee_set.count() == 3


def test_parse_row(db):
    user = UserFactory.create()
    assert user.coffee_set.count() == 0

    parse_row(user, DUMMY_ROW, 1)

    assert user.coffee_set.count() == 1
    coffee = user.coffee_set.first()

    assert coffee.tasting_notes.count() == 3


def test_parse_row_invalid_name(db):
    user = UserFactory.create()
    assert user.coffee_set.count() == 0

    invalid_name_row = copy.deepcopy(DUMMY_ROW)
    del invalid_name_row["coffee_name"]

    with pytest.raises(ValueError) as exc_info:
        parse_row(user, invalid_name_row, 1)

    assert "coffee_name is a required field in row 1" == str(exc_info.value)


def test_parse_row_invalid_processing(db):
    user = UserFactory.create()
    assert user.coffee_set.count() == 0

    row = copy.deepcopy(DUMMY_ROW)
    del row["processing"]

    with pytest.raises(ValueError) as exc_info:
        parse_row(user, row, 1)

    assert "processing is a required field in row 1" == str(exc_info.value)


def test_parse_row_invalid_roaster(db):
    user = UserFactory.create()
    assert user.coffee_set.count() == 0

    row = copy.deepcopy(DUMMY_ROW)
    del row["roaster"]

    with pytest.raises(ValueError) as exc_info:
        row["roasting_date"] = "2022.03.03"
        parse_row(user, row, 1)

    assert "roaster is a required field in row 1" == str(exc_info.value)


def test_parse_row_invalid_date(db):
    user = UserFactory.create()
    assert user.coffee_set.count() == 0
    invalid_date_row = copy.deepcopy(DUMMY_ROW)

    with pytest.raises(ValueError) as exc_info:
        invalid_date_row["roasting_date"] = "2022.03.03"
        parse_row(user, invalid_date_row, 1)

    assert "roasting_date is invalid in row 1" == str(exc_info.value)


def test_parse_roasting_date():
    date = datetime(2022, 3, 3).date()
    assert date == parse_roasting_date("2022-03-03")

    with pytest.raises(ValueError) as exc_info:
        parse_roasting_date("2022.03.03")

    assert "expected date format to be YYYY-MM-DD" == str(exc_info.value)


@pytest.mark.parametrize(
    ["notes_str", "expected"],
    [
        ("One, two,and three", ["One", "Two", "And three"]),
        ("Multiple words in one note", ["Multiple words in one note"]),
        ("WeIrD,UsE , of, CapItals", ["Weird", "Use", "Of", "Capitals"]),
    ],
)
def test_get_tasting_notes(notes_str, expected):
    assert expected == get_tasting_notes(notes_str)


def test_add_tasting_notes_to_coffee(db, setup_one_coffee):
    coffee = Coffee.objects.first()
    assert coffee.tasting_notes.count() == 0

    add_tasting_notes_to_coffee(coffee, ["Dark chocolate", "Floral", "Fruity", "Sweet"])

    assert coffee.tasting_notes.count() == 4
