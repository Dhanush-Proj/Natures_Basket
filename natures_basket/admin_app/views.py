from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from product_app.models import Product, Category, Subcategory,Image
from user_app.models import User, FarmerProfile, BuyerProfile
from cart_app.models import Order
from product_app.forms import ProductForm, CategoryForm, SubcategoryForm
from django.contrib import messages 
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.http import Http404
from product_app.forms import ImageForm

# Create your views here.

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == "admin":
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')
    return _wrapped_view


@admin_required
def admin_dashboard(request):
    # Get some key metrics for the admin dashboard
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_users = User.objects.count()
    total_farmers = FarmerProfile.objects.count()
    total_buyers = BuyerProfile.objects.count() 
    context = {
        'total_orders': total_orders,
        'total_products': total_products,
        'total_users': total_users,
        'total_farmers': total_farmers,
        'total_buyers': total_buyers,
    }
    return render(request, 'admin/dashboard.html',context)
               
@admin_required
def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'admin/product_list.html', context)

@admin_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()  # Save the product, get the instance
            return redirect('admin_app:image_create', product_id=product.pk)
    else:
        form = ProductForm()
    return render(request, 'admin/product_create.html', {'form': form})

@admin_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_app:admin_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/product_edit.html', {'form': form, 'product': product})

@admin_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin_app:admin_product_list')

class ImageListView(ListView):
    model = Image
    template_name = 'image_list.html'
    context_object_name = 'images'

    def get_queryset(self):
        self.product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        return Image.objects.filter(product=self.product)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.product
        return context

class ImageCreateView(CreateView):
    model = Image
    form_class = ImageForm
    template_name = 'admin/image_form.html'
    success_url=reverse_lazy('admin_app:admin_product_list')

    def form_valid(self, form):
        self.product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        image = form.save(commit=False)
        image.product = self.product
        image.save()
        return redirect('admin_app:admin_product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(Product, pk=self.kwargs['product_id'])
        return context

class ImageUpdateView(UpdateView):
    model = Image
    form_class = ImageForm
    template_name = 'image_form.html'

    def get_success_url(self):
        return reverse_lazy('image_list', kwargs={'product_id': self.object.product.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context

class ImageDeleteView(DeleteView):
    model = Image
    template_name = 'image_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('image_list', kwargs={'product_id': self.object.product.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context

@admin_required
def order_list(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'admin/order_list.html', context)

@admin_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'admin/order_detail.html', context)

@admin_required
def user_list(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'admin/user_list.html', context)

@admin_required
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {'user': user}
    return render(request, 'admin/user_detail.html', context)

@admin_required
def user_delete(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
    except Http404:
        messages.error(request, "User not found.")
        return redirect('admin_app:admin_user_list')

    if request.method == 'POST':
        try:
            user.delete()
            messages.success(request, f'User "{user.username}" deleted successfully.')
        except Exception as e:
            messages.error(request, f"Error deleting user: {e}")

        return redirect('admin_app:admin_user_list')

    context = {'user': user}
    return render(request, 'admin/user_confirm_delete.html', context)

@admin_required
def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'admin/category_list.html', context)

@admin_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES) #Important to include request.FILES for image uploads
        if form.is_valid():
            category = form.save(commit=False) #create the object, but don't save yet.
            if 'category_image' in request.FILES:
                category.category_image = request.FILES['category_image'] #manually save the image.
            category.save()
            messages.success(request, 'Category created successfully!')
            return redirect('admin_app:admin_category_list')
        else:
            messages.error(request, 'Error creating category. Please check the form.')
    else:
        form = CategoryForm()
    return render(request, 'admin/category_create.html', {'form': form})

@admin_required
def category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')  # Optional message
            return redirect('admin_app:admin_category_list')
        else:
            messages.error(request, 'Error updating category. Please check the form.') # Optional message
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin/category_edit.html', {'form': form, 'category': category})

@admin_required
def subcategory_list(request):
    subcategories = Subcategory.objects.all()
    context = {'subcategories': subcategories}
    return render(request, 'admin/subcategory_list.html', context)

@admin_required
def subcategory_create(request):
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subcategory created successfully!') # Optional message
            return redirect('admin_app:admin_subcategory_list')
        else:
            messages.error(request, 'Error creating subcategory. Please check the form.') # Optional message
    else:
        form = SubcategoryForm()
    return render(request, 'admin/subcategory_create.html', {'form': form})

@admin_required
def subcategory_edit(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subcategory updated successfully!') # Optional message
            return redirect('admin_app:admin_subcategory_list')
        else:
            messages.error(request, 'Error updating subcategory. Please check the form.') # Optional message
    else:
        form = SubcategoryForm(instance=subcategory)
    return render(request, 'admin/subcategory_edit.html', {'form': form, 'subcategory': subcategory})