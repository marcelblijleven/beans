from beans.apps.base.models import User


def get_aggregated_results(user: User) -> dict[str, int]:
    if user is None or not isinstance(user, User):
        raise ValueError("user must be an instance of User")

    return {
        "coffee": user.coffee_set.count(),
        "origins": user.coffee_set.values("country").distinct().count(),
        "roasters": user.roaster_set.count(),
    }
