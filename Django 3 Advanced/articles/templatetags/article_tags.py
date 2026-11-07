from django import template
from django.urls import reverse
from django.utils import translation

register = template.Library()


@register.filter
def short_synopsis(value):
    """Limit a synopsis to 20 characters, including three trailing dots."""
    value = str(value)
    return value if len(value) <= 20 else value[:17] + "..."


@register.simple_tag(takes_context=True)
def language_url(context, language):
    match = context["request"].resolver_match
    with translation.override(language):
        url = reverse(match.view_name, args=match.args, kwargs=match.kwargs)
    query = context["request"].GET.urlencode()
    return f"{url}?{query}" if query else url
