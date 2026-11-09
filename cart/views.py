from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product

def get_cart(request):
    """Get or create cart from session"""
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']

def view_cart(request):
    """Display shopping cart"""
    cart = get_cart(request)
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = float(product.price) * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    
    request.session['cart'] = cart
    messages.success(request, f'{product.name} added to cart!')
    return redirect('view_cart')


def update_cart(request, product_id):
    """Update product quantity in cart"""
    cart = get_cart(request)
    quantity = int(request.POST.get('quantity', 0))
    
    if quantity > 0:
        cart[product_id] = quantity
    else:
        cart.pop(product_id, None)
    
    request.session['cart'] = cart
    return redirect('view_cart')


def remove_from_cart(request, product_id):
    """Remove product from cart"""
    cart = get_cart(request)
    cart.pop(product_id, None)
    request.session['cart'] = cart
    
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')