from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from user_app.models import BuyerProfile
from cart_app.models import Order, OrderItem, ShippingAddress
from product_app.models import Product
from .models import Wishlist

# Create your views here.

@login_required
def buyer_dashboard(request):
    buyer = request.user.buyer_profile
    # Get recent orders for the buyer
    recent_orders = request.user.orders.all().order_by('-created_at')[:3] 
    wishlist_items = request.user.wishlist.all()
    context = {'recent_orders': recent_orders, 'wishlist_items': wishlist_items}
    return render(request, 'buyers/dashboard.html', context)

@login_required
def buyer_order_history(request):
    orders = request.user.orders.all()
    context = {'orders': orders}
    return render(request, 'buyers/order_history.html', context)

@login_required
def buyer_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'buyers/order_detail.html', context)

@login_required
def wishlist(request):
    wishlist_items = request.user.wishlist.all()
    context = {'wishlist_items': wishlist_items}
    return render(request, 'buyers/wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.wishlist.add(product)
    return redirect('product_detail', slug=product.slug)

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.wishlist.remove(product)
    return redirect('wishlist')

@login_required
def address_book(request):
    addresses = request.user.shippingaddress_set.all()
    context = {'addresses': addresses}
    return render(request, 'buyers/address_book.html', context)