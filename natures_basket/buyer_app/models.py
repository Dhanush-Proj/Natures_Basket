from django.db import models
from django.contrib.auth import get_user_model
from product_app.models import Product  # Import your Product model

# Create your models here.

User = get_user_model()

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, related_name='wishlists')  # Many-to-many with Product

    def __str__(self):
        return f"Wishlist for {self.user.username}"