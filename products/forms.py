from django import forms
from .models import ProductDetailsModel, ProductImageModel


class ProductDetailsForm(forms.ModelForm):
    """
    Form to handle product details for designers.
    """
    class Meta:
        model = ProductDetailsModel
        # fields = "__all__"
        exclude = ["designer"]
        
        widgets = {
            'product_description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'product_name': forms.TextInput(attrs={'placeholder': 'Enter product name'}),
            'product_category': forms.Select(attrs={'class': 'form-control'}),
            'product_price': forms.NumberInput(attrs={'placeholder': 'Enter price'}),
            
        }
        

class ProductImageForm(forms.ModelForm):
    """
    Form to handle multiple images for a product.
    """
    class Meta:
        model = ProductImageModel
        fields = '__all__'
        
        widgets = {
            'product_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
