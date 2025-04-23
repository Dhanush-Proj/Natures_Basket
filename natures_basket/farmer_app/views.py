from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from product_app.models import Product, Subcategory,Image, Category
from user_app.models import FarmerProfile
from cart_app.models import Order, OrderItem
from product_app.forms import ProductForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Prefetch
from user_app.models import FarmerProfile  # Import FarmerProfile

# Create your views here.
@login_required
def farmer_dashboard(request):
    try:
        farmer = request.user.farmer_profile  # Corrected line
        products = Product.objects.filter(subcategory__category__in=farmer.get_categories())
        context = {
            'farmer': farmer,
            'products': products,
        }
        return render(request, 'farmers/dashboard.html', context)
    except FarmerProfile.DoesNotExist:
        # Handle the case where the user doesn't have a FarmerProfile
        context = {
            'farmer': None,
            'products': [],
        }
        return render(request, 'farmers/dashboard.html', context)

@login_required
def farmer_product_list(request):
    farmer = request.user.farmer_profile
    products = Product.objects.filter(subcategory__category__in=farmer.get_categories())
    context = {'products': products}
    return render(request, 'farmers/product_list.html', context)

@login_required
def farmer_product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()

            # Correctly handle multiple image uploads (using a separate field)
            for image in request.FILES.getlist('images'):
                Image.objects.create(product=product, image=image)

            return redirect('farmer_product_list')
    else:
        form = ProductForm()
    return render(request, 'farmers/product_create.html', {'form': form})


@login_required
def farmer_product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.subcategory.category not in request.user.farmer_profile.get_categories():
        return HttpResponseForbidden() 

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('farmer_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'farmers/product_edit.html', {'form': form, 'product': product})

@login_required
def farmer_order_list(request):
    orders = Order.objects.filter(items__product__subcategory__category__in=request.user.farmer_profile.get_categories())
    context = {'orders': orders}
    return render(request, 'farmers/order_list.html', context)

@login_required
def farmer_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.filter(product__subcategory__category__in=request.user.farmer_profile.get_categories()) 
    context = {'order': order, 'order_items': order_items}
    return render(request, 'farmers/order_detail.html', context)

