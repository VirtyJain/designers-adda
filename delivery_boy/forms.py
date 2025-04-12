from django import forms
from .models import DeliveryBoyModel

class DeliveryBoyForm(forms.ModelForm):
    
    class Meta:
        model = DeliveryBoyModel
        exclude = ['user', 'is_business', 'is_verified', 'is_active', 'is_deleted']
        
        widgets = {
            'vehicle_no' : forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter Your Vehicle Number'}),
            'vehicle_name' : forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter Your Vehicle Model Name'}),
            'vehicle_type' : forms.Select(attrs={'class': 'input', 'placeholder': 'Choose Your Vehicle Type'}),
        }