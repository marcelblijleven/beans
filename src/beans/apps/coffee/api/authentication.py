from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    """
    Authentication class that uses Bearer instead of Token as keyword
    """

    keyword = "Bearer"
