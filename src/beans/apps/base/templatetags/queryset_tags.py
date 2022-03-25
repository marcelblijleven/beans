from django import template
from django.db.models import QuerySet, Count, F

from beans.apps.coffee.models import Coffee

register = template.Library()


@register.filter
def count_distinct_fields(queryset: QuerySet, field: str):
    return queryset.values(field).distinct().count()


@register.filter
def get_most_common_origins(queryset: QuerySet[Coffee], limit: int):
    return queryset.values("country").annotate(count=Count("country")).order_by("-count", "name")[:limit]


@register.filter
def get_most_common_roasters(queryset: QuerySet[Coffee], limit: int):
    return (
        queryset.values("roaster__name")
        .annotate(name=F("roaster__name"), count=Count("roaster__name"))
        .order_by("-count", "name")[:limit]
    )
