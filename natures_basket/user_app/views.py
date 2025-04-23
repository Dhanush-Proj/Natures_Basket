from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, UserProfileForm, FarmerProfileForm, BuyerProfileForm, AddressForm
from .models import User, FarmerProfile, BuyerProfile
from product_app.models import Category,Product,Subcategory,Image
from cart_app.models import ShippingAddress
from django import VERSION
from django.db.models import Prefetch


from django.http import HttpResponseRedirect

# Constants for user types (recommended)
USER_TYPE_ADMIN = 'admin'  # Or whatever your actual values are
USER_TYPE_BUYER = 'buyer'
USER_TYPE_FARMER = 'farmer'

def home(request):
    return render(request, 'home.html') 

def index(request):
    return render(request, 'index.html')

def homepage(request):
   
        categories = Category.objects.prefetch_related(
            Prefetch(
                'subcategory_set',
                queryset=Subcategory.objects.prefetch_related(
                    Prefetch(
                        'product_set',
                        queryset=Product.objects.prefetch_related(
                            Prefetch(
                                'images',  # Use the related_name here
                                queryset=Image.objects.all(),
                                to_attr='prefetched_images'
                            )
                        ),
                        to_attr='prefetched_products'
                    )
                ),
                to_attr='prefetched_subcategories'
            )
        ).all()

        context = {
            'categories': categories,
        }
        return render(request, 'homepage.html', context)


"""

    subcategories_prefetch = Prefetch(
        'subcategory_set',
        queryset=Subcategory.objects.all(),
        to_attr='prefetched_subcategories'
    )

    # Prefetch products within each subcategory
    products_prefetch = Prefetch(
        'prefetched_subcategories__product_set',
        queryset=Product.objects.all(),
        to_attr='prefetched_products'
    )
    images_prefetch = Prefetch(
        'prefetched_products__image_set', # Assumes Image model has ForeignKey to Product.
        queryset=Image.objects.all(),
        to_attr='prefetched_images'
    )

    categories = Category.objects.prefetch_related(subcategories_prefetch, products_prefetch, images_prefetch).all()


    context = {
        'categories': categories,
        
    }
 
 
 
    return render(request, 'homepage.html',context) 
 """
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = user.user_type # Get user_type from form
            if user_type == 'farmer':
                FarmerProfile.objects.create(user=user)
            elif user_type == 'buyer':
                BuyerProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('user_app:login')  # Redirect to the home page
        else:
            for field, errors in form.errors.items(): # Display form errors to user
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                # Correct Redirect Logic using reverse and user_type constants
                if user.user_type == USER_TYPE_ADMIN:
                    return HttpResponseRedirect(reverse('admin_app:admin_dashboard'))
                elif user.user_type == USER_TYPE_BUYER:
                    return HttpResponseRedirect(reverse('buyer_app:buyer_dashboard'))
                elif user.user_type == USER_TYPE_FARMER:
                    return HttpResponseRedirect(reverse('farmer_app:farmer_dashboard'))
                else:
                    return redirect(reverse('homepage')) 

            
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            messages.error(request, "\n".join(error_messages))

    else:  # GET request
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    
    return redirect('user_app:homepage')  # Redirect to the home page

@login_required  # Protect the profile view
def profile(request):
    user = request.user  # Get the current user
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user)  # Handle file uploads
        if hasattr(user, 'farmer_profile'):
            profile_form = FarmerProfileForm(request.POST, instance=user.farmer_profile)
        elif hasattr(user, 'buyer_profile'):
            profile_form = BuyerProfileForm(request.POST, instance=user.buyer_profile)
        else:
            profile_form = None  # Handle cases where the user has no profile yet

        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()): # Check both forms
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')  # Redirect to the profile page
        else:
            # Display form errors to user
            for form in [user_form, profile_form] :
                if form and form.errors:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"{field}: {error}")


    else:  # GET request
        user_form = UserProfileForm(instance=user)
        if hasattr(user, 'farmer_profile'):
            profile_form = FarmerProfileForm(instance=user.farmer_profile)
        elif hasattr(user, 'buyer_profile'):
            profile_form = BuyerProfileForm(instance=user.buyer_profile)
        else:
            profile_form = None

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def address_book(request):
    addresses = request.user.shippingaddress_set.all()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully!')
            return redirect('address_book')
    else:
        form = AddressForm()
    context = {'addresses': addresses, 'form': form}
    return render(request, 'accounts/address_book.html', context)

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully!')
            return redirect('address_book')
    else:
        form = AddressForm(instance=address)
    context = {'address': address, 'form': form}
    return render(request, 'accounts/edit_address.html', context)

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted successfully!')
    return redirect('address_book')