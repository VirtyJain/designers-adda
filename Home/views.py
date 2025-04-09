from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomerForm
from .models import CustomUser

# Create your views here.

def home_page(request):
    return render(request, template_name="home/home_page.html")


def register(request):
    return render(request, template_name="home/register.html")


def about(request):
    return render(request, template_name="home/about.html")


def logout_confirmation(request):
    return render(request, template_name="home/logout.html")


class CustomerFormView(generic.FormView):
    form_class = CustomerForm
    template_name = 'home/user_register.html'
    
    def form_valid(self, form):
        customer = form.save()
        return render(self.request, 'home/success.html', context = {'customer': customer})


class UserLoginView(LoginView):
    template_name = 'home/login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy('user_home_page')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home_page')
    

class UserDeleteView(generic.DeleteView):
    model = CustomUser
    template_name = "home/delete.html"
    success_url = reverse_lazy('home_page')