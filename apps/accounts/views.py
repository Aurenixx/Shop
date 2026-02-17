from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from apps.main.models import Category

# ----------------------
# Вхід користувача
# ----------------------
def login_view(request):
    # Якщо користувач вже авторизований — редірект на головну
    if request.user.is_authenticated:
        return redirect('main:product_list')

    form = AuthenticationForm(data=request.POST or None)
    next_url = request.GET.get('next', '')

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Редірект на next якщо є, інакше на головну
            if next_url:
                return redirect(next_url)
            return redirect('main:product_list')

    categories = Category.objects.all()
    return render(request, 'accounts/login.html', {
        'form': form,
        'categories': categories,
        'next': next_url,
    })

# ----------------------
# Вихід користувача
# ----------------------
def logout_view(request):
    logout(request)
    return redirect('main:product_list')

# ----------------------
# Реєстрація користувача
# ----------------------
def register_view(request):
    if request.user.is_authenticated:
        return redirect('main:product_list')

    form = UserCreationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:product_list')

    categories = Category.objects.all()
    return render(request, 'accounts/register.html', {
        'form': form,
        'categories': categories,
    })

# ----------------------
# Профіль користувача
# ----------------------
@login_required(login_url='accounts:login')
def profile_view(request):
    categories = Category.objects.all()
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'categories': categories,
    })


# ----------------------
# Middleware для захисту /admin/
# ----------------------
class AdminAccessRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated or not request.user.is_staff:
                return redirect('main:product_list')
        return self.get_response(request)
