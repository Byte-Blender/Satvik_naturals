from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category, CreativeUse

def product_list(request):
    """Display all products with pagination and filtering"""
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.all()
    
    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    products = products.order_by(sort)
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
    }
    return render(request, 'products/product_list.html', context)


def category_detail(request, slug):
    """Display products in a specific category"""
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(is_active=True)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'products/category_detail.html', context)


def product_detail(request, slug):
    """Display single product with details"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


def search_products(request):
    """Search products by name or description"""
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'products/search_results.html', context)


def home(request):
    """Satvik Naturals Homepage"""
    # Get 4 featured products for the Best Sellers section
    featured_products = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
    
    # Get Creative Uses for the how-to-use section
    creative_uses = CreativeUse.objects.filter(is_active=True).order_by('order')
    
    context = {
        'featured_products': featured_products,
        'creative_uses': creative_uses
    }
    return render(request, 'home.html', context)