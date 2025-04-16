from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.delivery_boy_home_page, name='delivery_boy_home_page'),
    path('about/', views.delivery_boy_about_page, name='delivery_boy_about_page'),
    path('profile/<int:pk>/', views.DeliveryBoyProfileView.as_view(), name='delivery_boy_profile'),
    
]
