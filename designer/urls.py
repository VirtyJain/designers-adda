from django.urls import path
from .views import DesignerFormView, DesignerBusinessFormView, home_view, DesignerDetailsView

urlpatterns = [
    path('register/', DesignerFormView.as_view(), name='designer_register'),
    path('business/', DesignerBusinessFormView.as_view(), name='designer_business_register'),
    path('home/', home_view, name='home'),
    path('details/<int:pk>/', DesignerDetailsView.as_view(), name='designer_details'),
]