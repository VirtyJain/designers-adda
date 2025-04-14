from django.urls import path
from . import views

urlpatterns = [
    path('register/<int:pk>/', views.DesignerFormView.as_view(), name='designer_register'),
    path('business/<int:pk>/', views.DesignerBusinessFormView.as_view(), name='designer_business_register'),
    path('home/', views.designers_home_view, name='designer_home_page'),
    path('profile/<int:pk>/', views.DesignerDetailsView.as_view(), name='designer_details'),
    path('update/<int:pk>/', views.DesignerDetailUpdateView.as_view(), name='designer_detail_update'),
    path('about/', views.about, name='about'),
    path('all_designers/', views.DesignerListView.as_view(), name='display_all_designers'),
    path('info/<int:pk>/', views.DesignerInfoView.as_view(), name='designer_info'),
    path('products/<int:pk>/', views.DesignerProductListView.as_view(), name='designer_products'),
    path('product/info/<int:pk>/', views.DesignerProductInfoView.as_view(), name='designer_product_info'),
    path('update_product/<int:pk>/', views.DesignerProductUpdateView.as_view(), name='designer_product_update'),
    path('delete_product/<int:pk>/', views.DesignerProductDeleteView.as_view(), name='designer_product_delete'),
    
]
