from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'cart_app'

urlpatterns = [
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/',views.view_cart,name='view_cart'),
        path('checkouts/', views.checkouts, name='checkouts'),

    path('checkout/', views.checkout, name='checkout'),
    path('order_history/', views.order_history, name='order_history'),
    path('order_detail/<str:order_id>/', views.order_detail, name='order_detail'),  # Note the <str:order_id>
    path('order_tracking/<str:order_id>/', views.order_tracking, name='order_tracking'), # Note the <str:order_id>
    path('process_payment/<int:order_id>/', views.process_payment, name='process_payment'), # If you pass order id as an integer
    path('process_payment/<str:order_id>/', views.process_payment, name='process_payment'), # If you pass order id as a string
        
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
