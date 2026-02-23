from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from apps.reviews.models import Review
from apps.reviews.forms import ReviewForm
from django.http import HttpResponseForbidden
from django.db.models import Count, Avg

def product_list(request, category_slug=None):
    categories = Category.objects.filter(is_active=True)
    category = None
    products = Product.objects.filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=category)

    search_query = request.GET.get("q")
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

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

    paginator = Paginator(products, 6)

    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        "products": products,
        "categories": categories,
        "category": category,
        "current_sort": sort_option,
        "search_query": search_query, 
    }
    return render(request, "main/product_list.html", context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, is_available=True)

    # Збільшуємо лічильник переглядів
    product.views += 1
    product.save(update_fields=["views"])

    # Схожі продукти
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    # Всі активні відгуки
    reviews = product.reviews.filter(is_active=True)
    reviews_count = reviews.count()

    # Визначаємо, чи користувач вже залишав відгук
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(author=request.user).first()

    # Форма для створення нового відгуку
    if request.method == "POST":
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.author = request.user
                review.save()
                return redirect(product.get_absolute_url())
        else:
            return HttpResponseForbidden("Потрібно увійти в акаунт")
    else:
        form = ReviewForm()

    raw_distribution = reviews.values('rating').annotate(count=Count('rating'))
    rating_distribution = {}
    for i in range(1, 6):
        rating_count = next((item['count'] for item in raw_distribution if item['rating'] == i), 0)
        percent = (rating_count / reviews_count * 100) if reviews_count else 0
        rating_distribution[i] = {'count': rating_count, 'percent': percent}

    average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0

    context = {
        "product": product,
        "related_products": related_products,
        "reviews": reviews,
        "reviews_count": reviews_count,
        "average_rating": average_rating,
        "rating_distribution": rating_distribution,
        "user_review": user_review,
        "form": form,
    }

    return render(request, "main/product_details.html", context)
