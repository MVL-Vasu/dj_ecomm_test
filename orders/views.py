from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from decimal import Decimal
from .models import Order, OrderItem
from cart.views import get_or_create_cart

@login_required
def order_history(request):
    """Display user's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_history.html', context)

@login_required
def order_detail(request, order_number):
    """Display order details"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)

def checkout(request):
    """Checkout process"""
    cart = get_or_create_cart(request)
    
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')
    
    context = {
        'cart': cart,
    }
    return render(request, 'orders/checkout.html', context)

@require_POST
def process_checkout(request):
    """Process checkout form submission"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to complete your order.')
        return redirect('accounts:login')
    
    cart = get_or_create_cart(request)
    
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')
    
    try:
        # Calculate totals
        subtotal = cart.total_price
        shipping_cost = Decimal('9.99')  # Fixed shipping cost
        tax_rate = Decimal('0.08')  # 8% tax
        tax_amount = (subtotal + shipping_cost) * tax_rate
        total_amount = subtotal + shipping_cost + tax_amount
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            
            # Billing Information
            billing_first_name=request.POST.get('billing_first_name'),
            billing_last_name=request.POST.get('billing_last_name'),
            billing_email=request.POST.get('billing_email'),
            billing_phone=request.POST.get('billing_phone'),
            billing_address_line_1=request.POST.get('billing_address_line_1'),
            billing_address_line_2=request.POST.get('billing_address_line_2', ''),
            billing_city=request.POST.get('billing_city'),
            billing_state=request.POST.get('billing_state'),
            billing_postal_code=request.POST.get('billing_postal_code'),
            billing_country=request.POST.get('billing_country'),
            
            # Shipping Information
            shipping_first_name=request.POST.get('shipping_first_name') or request.POST.get('billing_first_name'),
            shipping_last_name=request.POST.get('shipping_last_name') or request.POST.get('billing_last_name'),
            shipping_address_line_1=request.POST.get('shipping_address_line_1') or request.POST.get('billing_address_line_1'),
            shipping_address_line_2=request.POST.get('shipping_address_line_2') or request.POST.get('billing_address_line_2', ''),
            shipping_city=request.POST.get('shipping_city') or request.POST.get('billing_city'),
            shipping_state=request.POST.get('shipping_state') or request.POST.get('billing_state'),
            shipping_postal_code=request.POST.get('shipping_postal_code') or request.POST.get('billing_postal_code'),
            shipping_country=request.POST.get('shipping_country') or request.POST.get('billing_country'),
            
            # Order totals
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax_amount=tax_amount,
            total_amount=total_amount,
            
            # Payment info
            payment_method=request.POST.get('payment_method', 'card'),
            payment_status='paid',  # Assuming payment is successful
            order_status='processing',
            
            # Order notes
            order_notes=request.POST.get('order_notes', '')
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                product_price=cart_item.product.price,
                quantity=cart_item.quantity,
                total_price=cart_item.total_price
            )
        
        # Clear the cart
        cart.items.all().delete()
        
        messages.success(request, f'Order placed successfully! Your order number is {str(order.order_number)[:8]}.')
        return redirect('orders:order_detail', order_number=order.order_number)
        
    except Exception as e:
        messages.error(request, 'There was an error processing your order. Please try again.')
        return redirect('orders:checkout')
