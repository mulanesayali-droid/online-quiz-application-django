from django import template
import random

register = template.Library()

@register.filter
def shuffle(value):
    items = list(value)
    random.shuffle(items)
    return items
