from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def moeda_br(value):
    if value in (None, ""):
        return "0,00"

    try:
        amount = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return value

    sign = "-" if amount < 0 else ""
    amount = abs(amount)

    formatted = f"{amount:,.2f}"
    formatted = formatted.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"{sign}{formatted}"
