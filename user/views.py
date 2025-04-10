from django.shortcuts import render
from django.views import generic
from Home.forms import CustomerForm, CustomerChangeForm
from Home.models import CustomUser
from django.urls import reverse

# Create your views here.

def user_home_page(request):
    return render(request, template_name="user/home.html")


def about_page(request):
    return render(request, template_name="user/about.html")


class UserDetailView(generic.DetailView):
    model = CustomUser
    template_name = "user/customuser_detail.html"
    context_object_name = "user"
    

class UserUpdateView(generic.UpdateView):
    model = CustomUser
    form_class = CustomerChangeForm
    template_name = "user/customuser_update.html"
    success_url = '/user/profile/'

    def get_success_url(self):
        return reverse('user_profile', kwargs={'pk': self.object.pk})
