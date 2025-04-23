from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


app_name = 'user_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('index', views.index, name='index'),
    path('homepage', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),    
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('address_book/', views.address_book, name='address_book'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
