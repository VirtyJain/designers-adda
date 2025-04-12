from django.db import models
from Home.models import CustomUser
# Create your models here.

VEHICLE_CHOICES = (('Bike', 'Bike'), ('Scooty', 'Scooty'))

class DeliveryBoyModel(models.Model):
    """
    Model to store Delivery boy's details.
    """
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='delivery_boy')
    vehicle_no = models.CharField(max_length=15, verbose_name="Vehicle Number")
    vehicle_name = models.CharField(max_length=50, verbose_name="Vehicle Model Name")
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_CHOICES, default='Bike', verbose_name='Vehicle Type')
    driving_license = models.ImageField(upload_to='licenses/', verbose_name='Driving License')
    govt_id = models.ImageField(upload_to='govt_id/', verbose_name='Government Id Proof')
    salary = models.IntegerField(default=5000, verbose_name='Your salary')
    working_hours = models.IntegerField(default=10, verbose_name='Your Working Hours')
    
    def __str__(self):
        return self.user.username