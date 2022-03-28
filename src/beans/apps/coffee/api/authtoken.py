from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from beans.apps.coffee.api.serializers import AuthTokenSerializer


class EmailFieldObtainAuth(ObtainAuthToken):
    """
    ObtainAuth class that uses email field instead of username
    """

    throttle_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        email = data.get("email")
        password = data.get("password")
        user = authenticate(request, email=email, password=password)

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
