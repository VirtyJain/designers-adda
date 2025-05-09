from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/<int:pk>/', views.view_cart, name='view_cart'),
    path('place_order/<int:pk>/', views.place_order, name='place_order'),
    path('order_success/', views.order_success, name='order_success'),
    path('order_history/<int:pk>/', views.order_history, name='order_history'),
    path('order_product_info/<int:pk>/', views.OrderProductInfoView.as_view(), name='order_product_info'),
    path('payment_success', views.payment_success, name='payment_success'),
    path('payment_cancel', views.payment_cancel, name='payment_cancel'),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe_webhook'),

]
