from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('about/', views.about, name='about_page'),
    path('register/', views.register, name='register_page'),
    path('user_register/', views.CustomerFormView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='login_page'),
    path('logout_confirm/', views.logout_confirmation, name="logout_confirm"),
    path('logout/', views.UserLogoutView.as_view(), name='logout_page'),
    path('delete/<int:pk>/', views.UserDeleteView.as_view(), name='delete_page'),
    
]
