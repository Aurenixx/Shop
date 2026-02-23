from django.db import models
from django.urls import reverse
from django.db.models import Avg, Count

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Назва категорії")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Слаг")
    description = models.TextField(blank=True, verbose_name="Опис")
    image = models.ImageField(upload_to="categories/", blank=True, verbose_name="Зображення")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("main:product_list_by_category", args=[self.slug])
class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE, verbose_name="Категорія")
    name = models.CharField(max_length=150, verbose_name="Назва товару")
    slug = models.SlugField(unique=True, verbose_name="Слаг")
    description = models.TextField(verbose_name="Опис", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(upload_to="products/", blank=True, verbose_name="Зображення")
    views = models.IntegerField(default=0, verbose_name="Перегляди")
    featured = models.BooleanField(default=False, verbose_name="Рекомендований")
    is_available = models.BooleanField(default=True, verbose_name="В наявності")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def get_average_rating(self):
        return self.reviews.filter(is_active=True).aggregate(avg=Avg('rating'))['avg'] or 0

    def get_reviews_count(self):
        return self.reviews.filter(is_active=True).count()

    def get_rating_distribution(self):
        distribution = {i: 0 for i in range(1, 6)}
        ratings = self.reviews.filter(is_active=True).values('rating').annotate(
            count=Count('rating')
        )
        for item in ratings:
            distribution[item['rating']] = item['count']
        return distribution

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.id, self.slug])