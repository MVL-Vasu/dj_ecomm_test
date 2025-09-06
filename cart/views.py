from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Cart, CartItem
from products.models import Product

def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

def cart_detail(request):
    """Display cart details"""
    cart = get_or_create_cart(request)
    
    context = {
        'cart': cart,
    }
    return render(request, 'cart/cart_detail.html', context)

@require_POST
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request)
    
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
    except (json.JSONDecodeError, ValueError):
        quantity = 1
    
    if quantity <= 0:
        return JsonResponse({'success': False, 'message': 'Invalid quantity'})
    
    if quantity > product.stock_quantity:
        return JsonResponse({
            'success': False, 
            'message': f'Only {product.stock_quantity} items available'
        })
    
    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock_quantity:
            return JsonResponse({
                'success': False,
                'message': f'Cannot add more. Only {product.stock_quantity} items available'
            })
        cart_item.quantity = new_quantity
        cart_item.save()
    
    return JsonResponse({
        'success': True,
        'message': f'{product.name} added to cart',
        'cart_items_count': cart.total_items,
        'cart_total': str(cart.total_price)
    })

@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'message': 'Invalid quantity'})
    
    if quantity <= 0:
        cart_item.delete()
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart',
            'cart_items_count': cart.total_items
        })
    
    if quantity > cart_item.product.stock_quantity:
        return JsonResponse({
            'success': False,
            'message': f'Only {cart_item.product.stock_quantity} items available'
        })
    
    cart_item.quantity = quantity
    cart_item.save()
    
    return JsonResponse({
        'success': True,
        'message': 'Cart updated',
        'cart_items_count': cart.total_items,
        'item_total': str(cart_item.total_price),
        'cart_total': str(cart.total_price)
    })

@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    product_name = cart_item.product.name
    cart_item.delete()
    
    return JsonResponse({
        'success': True,
        'message': f'{product_name} removed from cart',
        'cart_items_count': cart.total_items,
        'cart_total': str(cart.total_price)
    })

@require_POST
def clear_cart(request):
    """Clear all items from cart"""
    cart = get_or_create_cart(request)
    cart.clear()
    
    return JsonResponse({
        'success': True,
        'message': 'Cart cleared',
        'cart_items_count': 0,
        'cart_total': '0.00'
    })
