from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "main"

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("products/category/<slug:category_slug>/", views.product_list, name="product_list_by_category"),
    path("product/<int:id>/<slug:slug>/", views.product_detail, name="product_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)