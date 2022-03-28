from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from beans.apps.base.templatetags.queryset_tags import get_most_common_roasters, get_most_common_origins
from beans.apps.coffee.models import Coffee, Roaster
from beans.apps.coffee.api.authentication import BearerTokenAuthentication
from beans.apps.coffee.api.serializers import RoasterSerializer, ProcessingSerializer, CoffeeSerializer


class AuthenticatedUserView(APIView):
    """
    Base view which requires authentication
    """

    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]


class CoffeeListView(AuthenticatedUserView):
    """
    List all coffees for the authenticated user
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Return a list of all coffees
        """
        coffees = request.user.coffee_set.all()
        serializer = CoffeeSerializer(coffees, many=True)
        return JsonResponse(serializer.data, safe=False)


class RoasterListView(AuthenticatedUserView):
    """
    List all roasters for the authenticated user
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Return a list of all roasters
        """
        roasters = request.user.roaster_set.all()
        serializer = RoasterSerializer(roasters, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProcessingListView(AuthenticatedUserView):
    """
    List all processing methods for the authenticated user
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Return a list of all the processing method
        """
        processing_methods = request.user.processing_set.all()
        serializer = ProcessingSerializer(processing_methods, many=True)
        return JsonResponse(serializer.data, safe=False)


class GenericStatsView(APIView):
    def _get(self, coffee_set: QuerySet[Coffee], roaster_set: QuerySet[Roaster], limit: int) -> JsonResponse:
        """
        Returns a stats dict for the provided QuerySets
        """
        top_roasters = get_most_common_roasters(coffee_set, limit).values("count", "name")
        top_origins = get_most_common_origins(coffee_set, limit).values("count", "origin")

        data = {
            "total_coffees": coffee_set.count(),
            "total_origins": coffee_set.values("country").distinct().count(),
            "total_roasters": roaster_set.count(),
            "top_origins": list(top_origins),
            "top_roasters": list(top_roasters),
        }

        # note: we can use safe=True because the data is just a dict
        return JsonResponse(data, safe=True)


class PublicStatsView(GenericStatsView):
    """
    Show site wide stats
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Returns site wide stats
        """
        limit = request.GET.get("limit", 5)
        coffee_set = Coffee.objects.all()
        roaster_set = Roaster.objects.all()
        return self._get(coffee_set, roaster_set, limit)


class UserStatsView(GenericStatsView, AuthenticatedUserView):
    """
    Show user stats
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Return the user's stats
        """
        limit = request.GET.get("limit", 5)
        coffee_set = request.user.coffee_set
        roaster_set = request.user.roaster_set
        return self._get(coffee_set, roaster_set, limit)
