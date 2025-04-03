from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import DesignerRegister, DesignerBusinessDetails


class DesignerRegisterForm(forms.ModelForm):
    
    """
    A form for creating new designer.
    """
    class Meta:
        model = DesignerRegister
        fields = "__all__"
        
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your bio'}),
            'certificate': forms.FileInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your years of experience'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your skills'}),
            'portfolio': forms.FileInput(attrs={'class': 'form-control'}),
            
        }
        
        
class DesignerBusinessDetailsForm(forms.ModelForm):
    
    """
    A form for creating new designer business details.
    """
    class Meta:
        model = DesignerBusinessDetails
        fields = "__all__"
        
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your business name'}),
            'business_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your business address'}),
            'business_contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your business contact number'}),
            'business_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your business email'}),
            'business_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your business description'}),
        }