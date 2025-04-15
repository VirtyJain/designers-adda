from django.contrib import admin
from .models import CartModel, OrderModel

# Register your models here.

@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'date_added')
    

@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'cart_product', 'total_price', 'order_status')