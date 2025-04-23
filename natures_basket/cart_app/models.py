from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.quantity * item.product.price  # Handle variant prices if needed
        return total

    def __str__(self):
        return f'Cart for {self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product_app.Product', on_delete=models.CASCADE)  # String reference
    variant = models.ForeignKey('product_app.Variant', on_delete=models.CASCADE, null=True, blank=True)  # String reference
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.variant:
            return f'{self.quantity} x {self.product.name} - {self.variant.name}'
        else:
            return f'{self.quantity} x {self.product.name}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=100, unique=True)  # Generate a unique order ID
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.quantity * item.price # Price is stored in OrderItem
        return total


    def __str__(self):
        return f'Order #{self.order_id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product_app.Product', on_delete=models.CASCADE)  # String reference
    variant = models.ForeignKey('product_app.Variant', on_delete=models.CASCADE, null=True, blank=True)  # String reference
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        if self.variant:
            return f'{self.quantity} x {self.product.name} - {self.variant.name}'
        else:
            return f'{self.quantity} x {self.product.name}'

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.address1}'
    
    class Meta:
        verbose_name_plural = "Shipping Addresses"  # More readable in admin
        ordering = ["-default"]  # Show default addresses first

    def save(self, *args, **kwargs):
        # Ensure only one default address per user
        if self.default:
            ShippingAddress.objects.filter(user=self.user).exclude(pk=self.pk).update(default=False)
        super().save(*args, **kwargs)


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, unique=True)  # Unique ID from the payment gateway
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for Order #{self.order.order_id}'