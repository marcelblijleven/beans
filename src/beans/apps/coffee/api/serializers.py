from rest_framework import serializers

from beans.apps.base.models import User
from beans.apps.coffee.models import Coffee, Processing, Roaster, TastingNote


class AuthTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = ["email", "password"]


class CoffeeSerializer(serializers.ModelSerializer):
    processing = serializers.SlugRelatedField(
        slug_field="name", many=False, queryset=Processing.objects.all(), read_only=False
    )
    roaster = serializers.SlugRelatedField(slug_field="name", many=False, queryset=Roaster.objects.all(), read_only=False)
    tasting_notes = serializers.SlugRelatedField(
        slug_field="name", many=True, queryset=TastingNote.objects.all(), read_only=False
    )

    class Meta:
        model = Coffee
        fields = [
            "name",
            "country",
            "processing",
            "roaster",
            "roasting_date",
            "rating",
            "variety",
            "tasting_notes",
        ]


class RoasterSerializer(serializers.ModelSerializer):
    coffees = serializers.IntegerField(source="coffee_set.count", read_only=True)

    class Meta:
        model = Roaster
        fields = ["id", "name", "country", "website", "coffees"]


class ProcessingSerializer(serializers.ModelSerializer):
    used = serializers.IntegerField(source="coffee_set.count", read_only=True)

    class Meta:
        model = Processing
        fields = ["id", "name", "used"]
