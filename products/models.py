from django.db import models
from designer.models import DesignerRegister

# Create your models here.

CATEGORY_CHOICES = (
    ('men_ethnic', "Men's Ethnic Wear"),
    ('men_casual', "Men's Casual Wear"),
    ('men_formal', "Men's Formal Wear"),
    ('women_ethnic', "Women's Ethnic Wear"),
    ('women_casual', "Women's Casual Wear"),
    ('women_formal', "Women's Formal Wear"),
)

class ProductDetailsModel(models.Model):
    """
    Model to store product details of specific designer.
    """
    designer = models.ForeignKey(DesignerRegister, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100, verbose_name='Product Name')
    product_description = models.TextField(verbose_name='Description')
    product_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Category')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    
    def __str__(self):
        return self.product_name
    

class ProductImageModel(models.Model):
    """
    Model to store multiple images of a product.
    """
    product = models.ForeignKey(ProductDetailsModel, on_delete=models.CASCADE, related_name='product_images')
    product_image = models.ImageField(upload_to='product_images/', verbose_name='Product Image')
    
    def __str__(self):
        return f"Image for {self.product.product_name}"
