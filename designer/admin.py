from django.contrib import admin
from .models import DesignerRegister, DesignerBusinessDetails

# Register your models here.

@admin.register(DesignerRegister)
class DesignerRegisterAdmin(admin.ModelAdmin):
    list_display = ['bio', 'skills', 'experience']
    
@admin.register(DesignerBusinessDetails)
class DesignerBusinessAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'business_address', 'business_contact_no']   