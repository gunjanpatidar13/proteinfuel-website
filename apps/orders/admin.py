from django.contrib import admin
from apps.orders.models import Order, OrderItem, OrderStatusHistory

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'product_name', 'quantity', 'unit_price', 'total_price')
    readonly_fields = ('product', 'product_name', 'quantity', 'unit_price', 'total_price')
    can_delete = False


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 1
    fields = ('status', 'changed_by', 'notes')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'customer_phone', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_phone', 'customer_email')
    readonly_fields = ('order_number', 'user', 'customer_name', 'customer_email', 'customer_phone', 'delivery_address_text', 'subtotal', 'tax', 'delivery_charge', 'total', 'created_at', 'updated_at')
    fieldsets = (
        ('Order Identification', {
            'fields': ('order_number', 'user', 'created_at')
        }),
        ('Customer Info', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Delivery Details', {
            'fields': ('delivery_address', 'delivery_address_text')
        }),
        ('Fulfillment Status', {
            'fields': ('status', 'notes')
        }),
        ('Financial Overview', {
            'fields': ('subtotal', 'tax', 'delivery_charge', 'total')
        }),
    )
    inlines = [OrderItemInline, OrderStatusHistoryInline]

    def save_model(self, request, obj, form, change):
        # Automatically log status changes in OrderStatusHistory
        if change:
            old_status = Order.objects.get(pk=obj.pk).status
            if old_status != obj.status:
                OrderStatusHistory.objects.create(
                    order=obj,
                    status=obj.status,
                    changed_by=request.user,
                    notes="Status updated via Django Admin."
                )
        super().save_model(request, obj, form, change)
