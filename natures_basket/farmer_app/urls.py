from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'farmer_app'

urlpatterns = [
    path('dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('products/', views.farmer_product_list, name='farmer_product_list'),
    path('products/create/', views.farmer_product_create, name='farmer_product_create'),
    path('products/edit/<int:product_id>/', views.farmer_product_edit, name='farmer_product_edit'),
    path('orders/', views.farmer_order_list, name='farmer_order_list'),
    path('orders/<int:order_id>/', views.farmer_order_detail, name='farmer_order_detail'),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
