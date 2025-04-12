from django.shortcuts import render

# Create your views here.

def delivery_boy_home_page(request):
    return render(request, template_name="delivery_boy/home.html")

def delivery_boy_about_page(request):
    return render(request, template_name="delivery_boy/about.html")