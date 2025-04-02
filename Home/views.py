from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request, template_name="home/home_page.html")


def register(request):
    return render(request, template_name="home/register.html")
