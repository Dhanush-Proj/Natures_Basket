from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Subcategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def product_list(request, category_slug=None, subcategory_slug=None):
    products = Product.objects.filter(is_active=True)

    category = None
    subcategory = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(subcategory__category=category)

    if subcategory_slug:
        subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
        products = products.filter(subcategory=subcategory)

    # Pagination
    paginator = Paginator(products, 10)  # Show 10 products per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'category': category if category_slug else None,
        'subcategory': subcategory if subcategory_slug else None,
    }
    return render(request, 'products/product_list.html', context)


# product_detail view
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    images = product.images.all()
    reviews = product.reviews.all()
    ratings = product.ratings.all()

    context = {
        'product': product,
        'images': images,
        'reviews': reviews,
        'ratings': ratings,
    }
    return render(request, 'products/product_detail.html', context)


def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'products/category_list.html', context)

def search(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    context = {'products': products, 'query': query}
    return render(request, 'products/search_results.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(subcategory__category=category)
    context = {'category': category, 'products': products}
    return render(request, 'products/category_detail.html', context)