from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem, ShippingAddress, Payment
from product_app.models import Product,Image
from .forms import CheckoutForm
from django.http import JsonResponse
import uuid  # For generating unique order IDs
from decimal import Decimal


# Create your views here.
def add_to_cart(request, product_id):
    """
    Adds an artwork to the user's cart using session.
    """
    product = get_object_or_404(Product, id=product_id)
    # Initialize or retrieve the cart from the session
    cart = request.session.get('cart', {})
    # Convert product_id to string for session storage (keys must be strings)
    product_id_str = str(product_id)
    image=get_object_or_404(Image, product_id=product_id)
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
       cart[product_id_str] = {
        'title': product.name,
        'price': float(product.price),  # Convert to float
        'quantity': int(1),  # Convert to int
        'image_url': image.image.url if image.image else None,
    } 
    request.session['cart'] = cart
    return redirect('user_app:homepage') 








def cart(request):
    """
    Retrieves cart items from the session and calculates totals.
    """
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = Decimal('0.00')  # Use Decimal for accurate price calculations
    total_items = 0

    for product_id_str, item_data in cart.items():
        try:
            product = get_object_or_404(Product, id=product_id_str) #or use Product.objects.get(pk=product_id_str)
            quantity = item_data.get('quantity', 0)
            price = Decimal(str(item_data.get('price', '0.00'))) #Convert to decimal

            item_total = int(price) *int( quantity)

            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
                'title': item_data.get('title'),
                'image_url': item_data.get('image_url'),
            })

            total_price += item_total
            total_items += quantity

        except Product.DoesNotExist:
            print(f"Warning: Product with ID {product_id_str} not found in database.")
        except Exception as e:
            print(f"An error occurred processing cart item {product_id_str}: {e}")

    return {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items,
    }

def update_cart(request, product_id, quantity):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart[str(product_id)] = int(quantity)  # Ensure quantity is an integer
        request.session['cart'] = cart
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session['cart'] = cart
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def view_cart(request):
    cart_items = []
    total_price = 0
    item_total=0
    cart = request.session.get('cart', {})


    for product_id, item_data in cart.items():     
        try:
            product = Product.objects.get(pk=product_id)
            

            quantity = item_data.get('quantity', 0)
            price = Decimal(str(item_data.get('price', '0.00'))) #Convert to decimal

            item_total = price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            })
            total_price += item_total
        except Product.DoesNotExist:
            del cart[product_id]
            request.session['cart'] = cart
            pass
    cart = request.session.get('cart', {})
    cart_item_count = len(cart.values())  # Calculate total items in cart
 
 
    context = {
        'cart_items': cart_items,
        'total_price': total_price, 'cart_item_count': cart_item_count,
    }
    return render(request, 'orders/cart.html', context) #replace cart.html with your template file name.


@login_required
def checkouts(request):
    form = CheckoutForm()
    cart_items = []
    total_price = 0
    cart = request.session.get('cart', {})

    for product_id, quantity in cart.items():
        print(quantity)
        try:
            product = Product.objects.get(pk=product_id)
            item_total =100
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            })
            total_price += item_total
        except Product.DoesNotExist:
            del cart[product_id]
            request.session['cart'] = cart
            return redirect('view_cart') #if you have a cart page.
            pass

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form, # Add form to the context
    }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            billing_details = form.save()
            order = Order.objects.create(
                user=request.user,
                billing_details=billing_details,
                total_amount=total_price,
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price,
                )
            request.session['cart'] = {} #clears the cart.
            
            # Redirect to a success page or order confirmation
            return redirect('user_app:homepage')  # Redirect to cart if no items

        else:
            # Re-render the form with errors
            context['form'] = form #include form with errors.
        return redirect('user_app:homepage')  # Redirect to cart if no items

    return redirect('user_app:homepage')  # Redirect to cart if no items

def checkout(request):
    cart = request.user.cart
    if not cart.items.exists():
        return redirect('cart')  # Redirect to cart if no items

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create ShippingAddress
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()

            # Create Order
            order = Order.objects.create(
                user=request.user,
                order_id=uuid.uuid4().hex[:10].upper()  # Generate a unique order ID
            )

            # Create OrderItems
            for item in cart.items.all():
                order_item = OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    variant=item.variant,
                    quantity=item.quantity,
                    price=item.product.price  # You might need to handle discounts or taxes here
                )

            # Clear cart
            cart.items.all().delete()

            # Redirect to payment gateway or order confirmation page
            # ... (Implement payment gateway integration here) ...
            return redirect('order_success', order_id=order.order_id)

    else:
        form = CheckoutForm()

    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_history(request):
    orders = request.user.orders.all()
    context = {'orders': orders}
    return render(request, 'orders/order_history.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'orders/order_detail.html', context)

@login_required
def order_tracking(request, order_id):
    # Implement order tracking logic here
    # For example, fetch tracking information from a third-party service
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    tracking_info = "Order is being processed."  # Placeholder
    context = {'order': order, 'tracking_info': tracking_info}
    return render(request, 'orders/order_tracking.html', context)

# Example payment processing function (replace with actual integration)
def process_payment(request, order):
    # ... (Integrate with your chosen payment gateway) ...
    # Example:
    if request.method == 'POST':
        # Get payment data from request
        # ...
        try:
            # Make payment request to the gateway
            # ...
            # If payment is successful:
            payment = Payment.objects.create(
                order=order,
                payment_method='credit_card',  # Replace with actual payment method
                amount=order.get_total(),  # Implement get_total() method in Order model
                # ... other payment details ...
            )
            order.is_paid = True
            order.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})