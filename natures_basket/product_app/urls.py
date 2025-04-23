from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('products/<slug:category_slug>/<slug:subcategory_slug>/', views.product_list, name='product_list_by_subcategory'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('search/', views.search, name='search'), 
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),   
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
