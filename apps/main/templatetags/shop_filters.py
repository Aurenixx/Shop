from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='currency')
def format_currency(value, currency='грн'):
    try:
        return f"{float(value):.2f} {currency}"
    except (ValueError, TypeError):
        return value

@register.filter
def discount_percentage(original_price, discount_price):
    try:
        original = float(original_price)
        discount = float(discount_price)
        if original <= 0:
            return 0
        return int(((original - discount) / original) * 100)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def compact_number(value):
    try:
        value = int(value)
        if value >= 1_000_000:
            return f"{value/1_000_000:.1f}M"
        elif value >= 1_000:
            return f"{value/1_000:.1f}K"
        return str(value)
    except (ValueError, TypeError):
        return value

@register.filter
def time_ago(date):
    if not date:
        return ""
    now = timezone.now()
    diff = now - date
    seconds = diff.total_seconds()
    if seconds < 60:
        return "щойно"
    elif seconds < 3600:
        return f"{int(seconds/60)} хв тому"
    elif seconds < 86400:
        return f"{int(seconds/3600)} год тому"
    elif seconds < 604800:
        return f"{int(seconds/86400)} дн тому"
    else:
        return date.strftime("%d.%m.%Y")
