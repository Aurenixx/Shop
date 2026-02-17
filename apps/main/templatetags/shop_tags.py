from django import template
from apps.main.models import Product

register = template.Library()

@register.simple_tag
def get_products_count(category=None):
    if category:
        return Product.objects.filter(category=category, is_available=True).count()
    return Product.objects.filter(is_available=True).count()

@register.simple_tag
def calculate_total(price, quantity):
    try:
        return float(price) * int(quantity)
    except (ValueError, TypeError):
        return 0

@register.simple_tag(takes_context=True)
def user_greeting(context):
    user = context.get('user')
    if user and user.is_authenticated:
        return f"Вітаємо, {user.username}!"
    return "Вітаємо, гість!"

@register.inclusion_tag('main/components/product_card.html')
def show_product_card(product):
    discount = 0
    if getattr(product, 'discount_price', None) and product.price > 0:
        discount = int(((product.price - product.discount_price) / product.price) * 100)
    return {
        'product': product,
        'discount': discount,
        'final_price': getattr(product, 'discount_price', None) or product.price
    }

@register.inclusion_tag('main/components/popular_products.html')
def show_popular_products(count=4):
    products = Product.objects.filter(is_available=True).order_by('-views')[:count]
    return {'popular_products': products}
