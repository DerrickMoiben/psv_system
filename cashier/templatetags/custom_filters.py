# your_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Template filter to get a value from a dictionary using a key."""
    return dictionary.get(key)