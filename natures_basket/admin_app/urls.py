from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'admin_app'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('products/', views.product_list, name='admin_product_list'),
    path('products/create/', views.product_create, name='admin_product_create'),
    path('products/edit/<int:product_id>/', views.product_edit, name='admin_product_edit'),
    path('products/delete/<int:product_id>/', views.product_delete, name='admin_product_delete'),
    path('product/<int:product_id>/images/', views.ImageListView.as_view(), name='image_list'),
    path('product/<int:product_id>/images/create/', views.ImageCreateView.as_view(), name='image_create'),
    path('image/update/<int:pk>/', views.ImageUpdateView.as_view(), name='image_update'),
    path('image/delete/<int:pk>/', views.ImageDeleteView.as_view(), name='image_delete'),
    path('orders/', views.order_list, name='admin_order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='admin_order_detail'),
    path('users/', views.user_list, name='admin_user_list'),
    path('users/<int:user_id>/', views.user_detail, name='admin_user_detail'),
    path('users/<int:user_id>/delete/', views.user_delete, name='admin_user_delete'),
    path('categories/', views.category_list, name='admin_category_list'),
    path('categories/create/', views.category_create, name='admin_category_create'),
    path('categories/edit/<int:category_id>/', views.category_edit, name='admin_category_edit'),
    path('subcategories/', views.subcategory_list, name='admin_subcategory_list'),
    path('subcategories/create/', views.subcategory_create, name='admin_subcategory_create'),
    path('subcategories/edit/<int:subcategory_id>/', views.subcategory_edit, name='admin_subcategory_edit'),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
