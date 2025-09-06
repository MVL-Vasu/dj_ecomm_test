from cart.models import Cart

def cart_context(request):
    """
    Context processor to make cart information available in all templates
    """
    cart_items_count = 0
    cart = None
    
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            if request.session.session_key:
                cart = Cart.objects.filter(session_key=request.session.session_key).first()
        
        if cart:
            cart_items_count = cart.total_items
    except:
        # In case of any error, just set defaults
        cart_items_count = 0
        cart = None
    
    return {
        'cart_items_count': cart_items_count,
        'cart': cart,
    }
