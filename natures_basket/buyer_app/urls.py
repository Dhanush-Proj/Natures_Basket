from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'buyer_app'

urlpatterns = [
    path('dashboard/buyer', views.buyer_dashboard, name='buyer_dashboard'),
    path('orders/', views.buyer_order_history, name='buyer_order_history'),
    path('orders/<int:order_id>/', views.buyer_order_detail, name='buyer_order_detail'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('address-book/', views.address_book, name='address_book'),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
