from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomerForm(UserCreationForm):
    class Meta:
        model = CustomUser
        exclude = ["is_active", "is_staff", "last_login", "is_superuser", "groups", "user_permissions", "password", "date_joined", "user_type"]
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your Last Name'}),
            'gender': forms.Select(attrs={'class': 'input'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'input', 'type': 'date', 'placeholder': 'Enter your date of birth'}),
            'age': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Enter your age'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Enter your email'}),
            'address': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your address'}),
            'contact_no': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your contact number'}),
            'image': forms.FileInput(attrs={'class': 'input'}),
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your username'}),
        }
