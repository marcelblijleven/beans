from beans.apps.base.templatetags.queryset_tags import (
    count_distinct_fields,
    get_most_common_origins,
    get_most_common_roasters,
)

from tests.factories.model_factories import UserFactory, CoffeeFactory, RoasterFactory


def test_count_distinct_fields(db, user_with_one_coffee):
    assert count_distinct_fields(user_with_one_coffee.roaster_set, "country") == 1
    user_with_one_coffee.roaster_set.create(name="test", country="test")
    assert count_distinct_fields(user_with_one_coffee.roaster_set, "country") == 2


def test_get_most_common_origins(db):
    user = UserFactory.create()
    CoffeeFactory.create(user=user, country="El Salvador")
    CoffeeFactory.create(user=user, country="Ethiopia")
    CoffeeFactory.create(user=user, country="Ethiopia")

    query_set = get_most_common_origins(user.coffee_set, 5)

    assert query_set.count() == 2
    assert query_set[0] == {"count": 2, "country": "Ethiopia"}
    assert query_set[1] == {"count": 1, "country": "El Salvador"}

    query_set = get_most_common_origins(user.coffee_set, 1)

    assert query_set.count() == 1


def test_get_most_common_roasters(db):
    user = UserFactory.create()
    roaster_a = RoasterFactory.create(user=user, name="roaster A")
    roaster_b = RoasterFactory.create(user=user, name="roaster B")
    CoffeeFactory.create(user=user, name="A1", roaster=roaster_a)
    CoffeeFactory.create(user=user, name="A2", roaster=roaster_a)
    CoffeeFactory.create(user=user, name="A3", roaster=roaster_a)
    CoffeeFactory.create(user=user, name="B1", roaster=roaster_b)
    CoffeeFactory.create(user=user, name="B2", roaster=roaster_b)

    query_set = get_most_common_roasters(user.coffee_set, 5)

    assert query_set.count() == 2
    assert query_set[0] == {"count": 3, "name": "roaster A", "roaster__name": "roaster A"}
    assert query_set[1] == {"count": 2, "name": "roaster B", "roaster__name": "roaster B"}
