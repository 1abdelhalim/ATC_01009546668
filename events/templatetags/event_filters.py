from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Split a string by the given separator.
    Example: {{ "a,b,c"|split:"," }}
    Returns: ['a', 'b', 'c']
    """
    if value:
        return value.split(arg)
    return [] 