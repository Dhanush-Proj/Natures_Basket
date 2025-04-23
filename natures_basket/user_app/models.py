from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _  # For translatable strings

# Create your models here.


class User(AbstractUser):
    USER_TYPE_CHOICES = (('buyer', _('Buyer')),('admin', _('Admin')),('farmer', _('Farmer')),)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer', verbose_name=_('User Type'))
    place = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Place'))
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone Number'))
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name=_('Profile Picture'))

    def __str__(self):
        return self.username


class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    farm_name = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)
    categories = models.ManyToManyField('product_app.Category') #added many to many field

    def __str__(self):
        return f'{self.user.username} - Farmer'

    def get_categories(self):
        return self.categories.all()


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    

    def __str__(self):
        return f'{self.user.username} - Buyer'