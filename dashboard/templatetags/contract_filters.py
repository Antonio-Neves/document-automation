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


@register.simple_tag
def gender(value, pair):
    """Return the masculine or feminine side of a 'masculine|feminine' pair."""

    masculine, separator, feminine = pair.partition('|')
    if not separator:
        return pair

    masculine = masculine.strip()
    feminine = feminine.strip()
    if not feminine:
        return masculine

    return feminine if (value or '').strip().lower() == 'feminine' else masculine
