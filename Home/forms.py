from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomerForm(UserCreationForm):
    
    """
    A form to create a new Customer.
    """
    
    contact_no = forms.CharField(
        required=True,
        max_length=10,
        validators=[
            RegexValidator(regex='^\d{10}$', message='Enter a valid 10-digit contact number.')
        ],
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Enter your contact number',
            'pattern': '[0-9]{10}',
            'maxlength': '10',
            'title': 'Enter exactly 10 digits'
        })
    )
    class Meta:
        model = CustomUser
        exclude = [ "is_active", "is_staff", "last_login", "is_superuser", "groups", "user_permissions", "password", "date_joined", "user_type"]
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your Last Name'}),
            'gender': forms.Select(attrs={'class': 'input'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'input', 'type': 'date', 'placeholder': 'Enter your date of birth'}),
            'age': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Enter your age'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Enter your email'}),
            'address': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your address'}),
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your username'}),
        }


class CustomerChangeForm(UserChangeForm):
    
    """
    A form to update the Customer's Profile Details.
    """
    
    contact_no = forms.CharField(
        required=True,
        max_length=10,
        validators=[
            RegexValidator(regex='^\d{10}$', message='Enter a valid 10-digit contact number.')
        ],
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Enter your contact number',
            'pattern': '[0-9]{10}',
            'maxlength': '10',
            'title': 'Enter exactly 10 digits'
        })
    )
    
    class Meta:
        model = CustomUser
        exclude = ["password", "is_active", "is_staff", "last_login", "is_superuser", "groups", "user_permissions", "date_joined", "user_type"]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your Last Name'}),
            'gender': forms.Select(attrs={'class': 'input'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'age': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Enter your age'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Enter your email'}),
            'address': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your address'}),
            'image': forms.FileInput(attrs={'class': 'input'}),
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)
