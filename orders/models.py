from django.db import models
from Home.models import CustomUser
from products.models import ProductDetailsModel
from Home.models import CustomUser

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
    order_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default='Pending', verbose_name="Order Status")

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"