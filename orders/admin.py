from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'order_status', 'payment_status', 'created_at']
    list_filter = ['order_status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__username', 'billing_email']
    inlines = [OrderItemInline]
    readonly_fields = ['order_number', 'total_items']
    fieldsets = (
        ('Order Info', {
            'fields': ('order_number', 'user', 'order_status', 'payment_status', 'payment_method')
        }),
        ('Billing Info', {
            'fields': ('billing_first_name', 'billing_last_name', 'billing_email', 
                      'billing_phone', 'billing_address_line_1', 'billing_address_line_2',
                      'billing_city', 'billing_state', 'billing_postal_code', 'billing_country')
        }),
        ('Shipping Info', {
            'fields': ('shipping_first_name', 'shipping_last_name', 'shipping_address_line_1',
                      'shipping_address_line_2', 'shipping_city', 'shipping_state',
                      'shipping_postal_code', 'shipping_country', 'tracking_number')
        }),
        ('Order Details', {
            'fields': ('subtotal', 'shipping_cost', 'tax_amount', 'total_amount', 'order_notes')
        })
    )
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'product_price', 'total_price']
    list_filter = ['order__created_at']
    search_fields = ['order__order_number', 'product_name']
