from django.contrib import admin
from .models import DeliveryBoyModel
# Register your models here.

@admin.register(DeliveryBoyModel)
class DeliveryBoyAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle_no', 'vehicle_name', 'vehicle_type', 'driving_license', 'govt_id']