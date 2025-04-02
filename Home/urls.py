from django.urls import path
from .views import home_page, register, CustomerFormView, UserLoginView

urlpatterns = [
    path('', home_page, name='home_page'),
    path('register/', register, name='register_page'),
    path('user_register/', CustomerFormView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='login_page'),
    
]
