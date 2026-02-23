from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.main.urls", namespace="main")),
    path('', include('apps.accounts.urls', namespace='accounts')),
    path("contact/", include("apps.contact.urls", namespace="contact")),
    path('reviews/', include('apps.reviews.urls'))
]
