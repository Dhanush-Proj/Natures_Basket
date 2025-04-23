from django import template
from product_app.models import Category  # Replace with your actual Category model

register = template.Library()

@register.inclusion_tag('category_list.html')
def show_categories(max_categories=None):
    """
    Displays a list of categories.
    """
    if max_categories:
        categories = Category.objects.all()[:max_categories]
    else:
        categories = Category.objects.all()
    return {'categories': categories}

@register.simple_tag
def category_count():
    """
    Returns the total number of categories.
    """
    return Category.objects.count()

@register.inclusion_tag('category_list_hierarchy.html')
def show_categories_hierarchy(parent=None):
    """
    Displays hierarchical categories.
    """
    if parent:
        categories = Category.objects.filter(parent=parent)
    else:
        categories = Category.objects.filter(parent__isnull=True) #top level categories

    return {'categories': categories}

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''  # Or handle the error as you see fit
 

@register.filter(name='shipping')
def shipping(cart):
    total = 0
    for item in cart.values():
        total += item['price'] * item['quantity']
    try:
        return float(total) * .005
    except (ValueError, TypeError):
        return ''  # Or handle the error as you see fit
 
@register.filter(name='total_cart_price')
def total_cart_price(cart):
    """Calculates the total price of the items in the cart."""
    total = 0
    for artwork_id, artwork_data in cart.items():
        total += artwork_data['price'] * artwork_data['quantity']
    return total

@register.filter
def cart_total(cart):
    total = 0
    for item in cart.values():
        total += item['price'] * item['quantity']
    return total