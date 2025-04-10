from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.DesignerFormView.as_view(), name='designer_register'),
    path('business/', views.DesignerBusinessFormView.as_view(), name='designer_business_register'),
    path('home/', views.designers_home_view, name='home'),
    path('profile/<int:pk>/', views.DesignerDetailsView.as_view(), name='designer_details'),
    path('update/<int:pk>/', views.DesignerDetailUpdateView.as_view(), name='designer_detail_update'),
    path('about/', views.about, name='about'),
]
