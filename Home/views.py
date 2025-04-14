from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
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
        
        send_mail(
            subject = 'Welcome to Designer’s Adda!',
            message = f'{customer.first_name}, Thank you for registering with Designer’s Adda. Your registration was successful.\n\nVisit the website and login to continue.',
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [customer.email],
            fail_silently = False,
        )
        
        return render(self.request, 'home/success.html', context = {'customer': customer})


class UserLoginView(LoginView):
    template_name = 'home/login.html'
    form_class = AuthenticationForm
    
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        if user.user_type == 'Customer':
            return redirect('user_home_page')
        elif user.user_type == 'Designer':
            return redirect('designer_home_page')
        elif user.user_type == 'Delivery_boy':
            return redirect('delivery_boy_home_page')
   

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home_page')
    

class UserDeleteView(generic.DeleteView):
    model = CustomUser
    template_name = "home/delete.html"
    success_url = reverse_lazy('home_page')