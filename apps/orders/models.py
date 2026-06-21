import uuid
from django.db import models
from apps.users.models import User, Address
from apps.catalog.models import Product
from apps.core.models import TimeStampedModel, SoftDeleteModel

class Order(TimeStampedModel, SoftDeleteModel):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Payment/Review'),
        ('CONFIRMED', 'Confirmed'),
        ('PREPARING', 'In the Kitchen / Preparing'),
        ('READY', 'Ready for Delivery/Pickup'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order_number = models.CharField(max_length=50, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    
    # Customer Details Snapshot (to prevent data loss if profile updates)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    
    # Delivery Snapshot
    delivery_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    delivery_address_text = models.TextField(help_text="Snapshot of address at time of order")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Pricing Snapshots
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    notes = models.TextField(blank=True, null=True, help_text="Cooking or delivery instructions")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number or self.id} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate a clean, readable order number prefix
            self.order_number = f"PF-{timezone_now_prefix()}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="order_items")
    product_name = models.CharField(max_length=150, help_text="Snapshot of product name")
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_name} in {self.order.order_number}"

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_history")
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Order Status Histories"
        ordering = ['-changed_at']

    def __str__(self):
        return f"Order {self.order.id} status changed to {self.status} at {self.changed_at}"


def timezone_now_prefix():
    from django.utils import timezone
    return timezone.now().strftime("%Y%m%d")
