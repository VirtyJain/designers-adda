from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomerForm(UserCreationForm):
    class Meta:
        model = CustomUser
        exclude = ["is_active", "is_staff", "last_login", "is_superuser", "groups", "user_permissions", "password"]
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Last Name'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your age'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your contact number'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
        }
