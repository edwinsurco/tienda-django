from django import template

register = template.Library()

@register.filter
def get_item(carrito, key):
    return carrito.get(str(key), {}).get('cantidad', 0)