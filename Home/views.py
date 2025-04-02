from django.shortcuts import render
from django.views import generic
# from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import CustomerForm, LoginForm

# Create your views here.

def home_page(request):
    return render(request, template_name="home/home_page.html")


def register(request):
    return render(request, template_name="home/register.html")


class CustomerFormView(generic.FormView):
    form_class = CustomerForm
    template_name = 'home/user_register.html'
    
    def form_valid(self, form):
        customer = form.save()
        return render(self.request, 'home/success.html', context = {'customer': customer})


class UserLoginView(LoginView):
    template_name = 'home/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('home_page')
