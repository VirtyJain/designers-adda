from django import forms
from .models import DesignerRegister, DesignerBusinessDetails


class DesignerRegisterForm(forms.ModelForm):
    
    """
    A form for creating new designer.
    """
    class Meta:
        model = DesignerRegister
        fields = "__all__"
        exclude = ['user', 'is_designer', 'is_business', 'is_verified', 'is_active', 'is_deleted']
        
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your bio'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your years of experience'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your skills'}),            
        }
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        
class DesignerBusinessDetailsForm(forms.ModelForm):
    
    """
    A form for creating new designer business details.
    """
    class Meta:
        model = DesignerBusinessDetails
        fields = "__all__"
        exclude = ['designer']
        
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your business name'}),
            'business_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your business address'}),
            'business_contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your business contact number'}),
            'business_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your business email'}),
            'business_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your business description'}),
        }