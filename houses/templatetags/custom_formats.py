from decimal import Decimal
from django import template


register = template.Library()


@register.filter
def format_number(value):
    if not isinstance(value, Decimal):
        return value

    return f"{value:,}"
