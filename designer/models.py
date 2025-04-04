from django.db import models
from Home.models import CustomUser
from django.contrib.auth.models import Group
# Create your models here.


class DesignerRegister(models.Model):

    """
    Model to store designer's details.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='designer')
    bio = models.TextField(verbose_name='Bio')
    certificate = models.FileField(upload_to='designer/certificate/', verbose_name='Certificate', null=True, blank=True)
    experience = models.IntegerField(verbose_name='Experience in years')
    skills = models.CharField(max_length=255, verbose_name='Skills')
    portfolio = models.FileField(upload_to='designer/portfolio/', verbose_name='Portfolio', null=True, blank=True)
    
    USERNAME_FIELD = 'user'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    

class DesignerBusinessDetails(models.Model):

    """
    Model to store business details of the designer.
    """
    designer = models.ForeignKey(DesignerRegister, on_delete=models.CASCADE, related_name='designer_business_details')
    business_name = models.CharField(max_length=255, verbose_name='Name')
    business_address = models.TextField(verbose_name='Address')
    business_contact_no = models.CharField(max_length=15, verbose_name='Contact Number')
    business_email = models.EmailField(verbose_name='Email')
    business_description = models.TextField(verbose_name='Description')
    
    def __str__(self):
        return f"{self.business_name} by {self.designer.user.first_name} {self.designer.user.last_name}"