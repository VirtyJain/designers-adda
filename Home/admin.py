from django.contrib import admin

# Register your models here.

from .models import Customer
from django.contrib.auth.admin import UserAdmin
@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    list_display=["username"]
    