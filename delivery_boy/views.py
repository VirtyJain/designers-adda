from django.shortcuts import render
from django.views import generic
from orders import models
from .models import DeliveryBoyModel
from Home.views import LoginRequiredBaseView

# Create your views here.

def delivery_boy_home_page(request):
    delivery_boy = DeliveryBoyModel.objects.get(user=request.user)
    delivery_boy_id = delivery_boy.id
    orders = models.OrderModel.objects.filter(delivery_boy=delivery_boy).select_related('user', 'cart_product__product')

    return render(request, 'delivery_boy/home.html', {
        'delivery_boy_id': delivery_boy_id,
        'orders': orders,
    })

def delivery_boy_about_page(request):
    return render(request, template_name="delivery_boy/about.html")


class DeliveryBoyProfileView(LoginRequiredBaseView, generic.DetailView):
    
    """
    view to display delivery boy profile.
    """
    
    model = DeliveryBoyModel
    context_object_name = 'delivery_boy'
    template_name = 'delivery_boy/delivery_boy_profile.html'