from django import template

register = template.Library()

@register.filter
def format_number(value):
    try:
        value = float(value)
        if value >= 1_000_000_000:
            return "${:.2f}B".format(value / 1_000_000_000)
        elif value >= 1_000_000:
            return "${:.2f}M".format(value / 1_000_000)
        elif value >= 1_000:
            return "${:.2f}K".format(value / 1_000)
        else:
            return "${:.2f}".format(value)
    except (ValueError, TypeError):
        return value
