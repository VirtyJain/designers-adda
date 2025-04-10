from django.urls import path
from .views import user_home_page, about_page, UserDetailView, UserUpdateView

urlpatterns = [
    path('home/', user_home_page, name='user_home_page'),
    path('about/', about_page, name='user_about_page'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='user_profile'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update_profile'),
]
