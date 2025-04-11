from django.urls import path
from . import views

urlpatterns = [
    path('form/', views.ProductDetailsView.as_view(), name='product_details'),
    path('success/', views.success_url, name='design_success'),
    path('list/', views.ProductListView.as_view(), name='product_list'),
    path('info/<int:pk>/', views.ProductInfoView.as_view(), name='product_info'),
    
]
