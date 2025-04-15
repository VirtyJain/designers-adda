from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

GENDERS_CHOICES = (('Male','Male'), ('Female', 'Female'), ('Other', 'Other'))
USER_TYPE = (('Customer', 'Customer'), ("Designer", 'Designer'), ("Delivery_boy", 'Delivery_boy'))

class BaseClass(AbstractUser):
    
    """
    A base user model for all the user's personal details.
    """
    gender = models.CharField(max_length=10, choices=GENDERS_CHOICES, default='M', verbose_name="Gender")
    date_of_birth = models.DateField(verbose_name="Date of Birth", null=True)
    age = models.IntegerField(verbose_name="Age", null=True)
    address = models.CharField(max_length=100, verbose_name="Address", null=True)
    contact_no = models.IntegerField(verbose_name="Contact Number", null=True)
    image = models.ImageField(upload_to='images/', verbose_name="Profile", null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE, default='Customer', verbose_name="User Type")

    class Meta:
        abstract = True


class CustomUser(BaseClass):
    
    """
    Model to store the customer's details.
    """
    pass

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
