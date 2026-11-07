from django import template

register = template.Library()


@register.filter
def short_synopsis(value):
    """Limit a synopsis to 20 characters, including three trailing dots."""
    value = str(value)
    return value if len(value) <= 20 else value[:17] + "..."
