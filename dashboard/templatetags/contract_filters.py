from django import template

register = template.Library()


@register.filter
def fill(value, width=20):
    """Return the field value stripped,
    or underscores of the given width if empty."""

    value = (value or '').strip()
    if value:
        return value
    return '_' * width
