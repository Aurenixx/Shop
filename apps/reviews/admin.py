from django.contrib import admin
from .models import Review


@admin.action(description="Активувати вибрані відгуки")
def activate_reviews(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Деактивувати вибрані відгуки")
def deactivate_reviews(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'product',
        'rating',
        'title_preview',
        'created_at',
        'is_active',
        'helpful_count'
    )

    list_filter = ('rating', 'is_active', 'created_at')
    search_fields = ('author__username', 'product__name', 'title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_active',)
    actions = [activate_reviews, deactivate_reviews]

    fieldsets = (
        ('Основна інформація', {
            'fields': ('product', 'author', 'rating', 'title', 'content')
        }),
        ('Додаткова інформація', {
            'fields': ('advantages', 'disadvantages')
        }),
        ('Модерація', {
            'fields': ('is_active', 'helpful_count')
        }),
        ('Дати', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def title_preview(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title