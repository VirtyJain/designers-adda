from django.shortcuts import render
from django.views import generic
from Home.models import CustomUser

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
    template_name = "user/customuser_detail.html"
    context_object_name = "user"
    fields = '__all__'
    success_url = '/user/profile/'