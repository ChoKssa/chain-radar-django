from django import template

# Register this file as a Django template filter module
register = template.Library()

@register.filter
def format_number(value):
    # Format large numbers into human-readable currency strings
    try:
        value = float(value)
        if value >= 1_000_000_000:
            return "${:.2f}B".format(value / 1_000_000_000)  # Format billions
        elif value >= 1_000_000:
            return "${:.2f}M".format(value / 1_000_000)      # Format millions
        elif value >= 1_000:
            return "${:.2f}K".format(value / 1_000)          # Format thousands
        else:
            return "${:.2f}".format(value)                   # Format small values normally
    except (ValueError, TypeError):
        # Return original value if conversion fails
        return value
