from django.db import models
from Home.models import CustomUser
from products.models import ProductDetailsModel
from Home.models import CustomUser
from delivery_boy.models import DeliveryBoyModel

# Create your models here.

class CartModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(ProductDetailsModel, on_delete=models.CASCADE, related_name='cart')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"
    

ORDER_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Dispatched', 'Dispatched'),
    ('Delivered', 'Delivered'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
    ('Refunded', 'Refunded'),
]
class OrderModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    cart_product = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='orders')
    delivery_boy = models.ForeignKey(DeliveryBoyModel, on_delete=models.SET_NULL, blank=True, null=True, related_name='delivery_boy')
    order_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    address = models.TextField()
    house_no = models.PositiveIntegerField()
    landmark = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default='Pending', verbose_name="Order Status")

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    

PAYMENT_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Failed', 'Failed'),
]
   
class PaymentModel(models.Model):
    order = models.OneToOneField(OrderModel, on_delete=models.CASCADE)
    stripe_payment_intent = models.CharField(max_length=255, null=True, blank=True)
    stripe_checkout_session_id = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=15,choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for Order {self.order.id} - Status: {self.payment_status}"
