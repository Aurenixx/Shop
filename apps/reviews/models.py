from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Review(models.Model):
    RATING_CHOICES = [(1,'1 ⭐'),(2,'2 ⭐⭐'),(3,'3 ⭐⭐⭐'),(4,'4 ⭐⭐⭐⭐'),(5,'5 ⭐⭐⭐⭐⭐')]

    product = models.ForeignKey(
        'main.Product',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES,
                                 validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    advantages = models.TextField(blank=True)
    disadvantages = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    helpful_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ['product','author']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username} - {self.product.name} ({self.rating}⭐)"

    def get_rating_display_stars(self):
        return '⭐' * self.rating