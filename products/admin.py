from django.contrib import admin
from .models import ProductDetailsModel, ProductImageModel

# Register your models here.

@admin.register(ProductDetailsModel)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_description']
    
@admin.register(ProductImageModel)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product_image']