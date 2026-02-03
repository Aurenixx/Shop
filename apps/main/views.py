from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request, category_slug=None):
    categories = Category.objects.filter(is_active=True)
    category = None
    products = Product.objects.filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=category)

    sort_option = request.GET.get("sort", "new")
    if sort_option == "new":
        products = products.order_by("-created_at")
    elif sort_option == "old":
        products = products.order_by("created_at")
    elif sort_option == "popular":
        products = products.order_by("-views")
    elif sort_option == "price_low":
        products = products.order_by("price")
    elif sort_option == "price_high":
        products = products.order_by("-price")
    elif sort_option == "name":
        products = products.order_by("name")
    else:
        products = products.order_by("-created_at")

    context = {
        "products": products,
        "categories": categories,
        "category": category,
        "current_sort": sort_option
    }
    return render(request, "main/product-list.html", context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, is_available=True)

    product.views += 1
    product.save(update_fields=["views"])

    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    context = {
        "product": product,
        "related_products": related_products
    }
    return render(request, "main/product-detail.html", context)
