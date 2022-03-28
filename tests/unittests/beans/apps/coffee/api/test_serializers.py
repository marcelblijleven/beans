from beans.apps.coffee.api.serializers import AuthTokenSerializer, CoffeeSerializer, RoasterSerializer, ProcessingSerializer

from tests.factories.model_factories import ProcessingFactory, RoasterFactory, CoffeeFactory, UserFactory


def test_auth_token_serializer(db, faker_person, settings):
    data = {
        "email": faker_person.email(),
        "password": faker_person.password(),
    }

    serializer = AuthTokenSerializer(data=data)
    assert serializer.is_valid()


def test_coffee_serializer(db):
    user = UserFactory.create()
    roaster = RoasterFactory.create(user=user)
    processing = ProcessingFactory.create(user=user)
    coffee = CoffeeFactory.create(user=user, roaster=roaster, processing=processing, country="Lesotho")

    serializer = CoffeeSerializer(coffee, many=False)
    assert serializer.data == {
        "country": "Lesotho",
        "name": "A Coffee",
        "processing": "Natural",
        "rating": 4,
        "roaster": "A roaster",
        "roasting_date": "2022-03-23",
        "tasting_notes": [],
        "variety": None,
    }


def test_roaster_serializer(db):
    user = UserFactory.create()
    roaster = RoasterFactory.create(user=user)
    serializer = RoasterSerializer(roaster, many=False)
    assert serializer.data == {"id": 1, "name": "A roaster", "country": "", "website": None, "coffees": 0}


def test_processing_serializer(db):
    user = UserFactory.create()
    processing = ProcessingFactory.create(user=user)
    serializer = ProcessingSerializer(processing, many=False)
    assert serializer.data == {"id": 1, "name": "Natural", "used": 0}
