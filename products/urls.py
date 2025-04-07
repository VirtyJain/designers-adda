from django.urls import path
from .views import ProductDetailsView, success_url

urlpatterns = [
    path('details/', ProductDetailsView.as_view(), name='product_details'),
    path('success/', success_url, name='design_success')
]
