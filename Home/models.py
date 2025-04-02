from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

GENDERS_CHOICES = (('M','Male'), ('F', 'Female'), ('O', 'Other'))


class BaseClass(AbstractUser):
    
    """
    A base user model for all the user's personal details
    """
    gender = models.CharField(max_length=10, choices=GENDERS_CHOICES, default='M', verbose_name="Gender")
    date_of_birth = models.DateField(verbose_name="Date of Birth", null=True)
    age = models.IntegerField(verbose_name="Age", null=True)
    address = models.CharField(max_length=100, verbose_name="Address", null=True)
    contact_no = models.IntegerField(verbose_name="Contact Number", null=True)
    image = models.ImageField(upload_to='images/', verbose_name="Profile", null=True, blank=True)

    class Meta:
        abstract = True


class Customer(BaseClass):
    pass
