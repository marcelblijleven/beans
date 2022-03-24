import pytest

from beans.apps.base.utils import get_aggregated_results


def test_get_aggregated_results(db, user_with_one_coffee):
    expected = {'coffee': 1, 'origins': 1, 'roasters': 1}
    assert expected == get_aggregated_results(user_with_one_coffee)


def test_get_aggregated_results_new_user(db, django_user_model):
    new_user = django_user_model.objects.create(email="test@email.com")
    expected = {'coffee': 0, 'origins': 0, 'roasters': 0}
    assert expected == get_aggregated_results(new_user)


def test_get_aggregated_results_invalid_user(anonymous_user):
    with pytest.raises(ValueError) as exc_info:
        get_aggregated_results(None)  # noqa

    assert "user must be an instance of User" == str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        get_aggregated_results(anonymous_user)  # noqa

    assert "user must be an instance of User" == str(exc_info.value)
