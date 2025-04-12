from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/<int:pk>/', views.view_cart, name='view_cart'),
]
