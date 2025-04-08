from django.shortcuts import render
from django.views import generic
from .forms import DesignerRegisterForm, DesignerBusinessDetailsForm
from .models import DesignerRegister
# Create your views here.


class DesignerFormView(generic.FormView):
    form_class = DesignerRegisterForm
    template_name = 'designer/designer_register.html'
    
    def form_valid(self, form):
        designer = form.save()
        return render(self.request, 'designer/business_details.html', context = {'designer': designer})
    

class DesignerBusinessFormView(generic.CreateView):
    form_class = DesignerBusinessDetailsForm
    template_name = 'designer/business_details.html'
    
    def form_valid(self, form):
        business = form.save()
        return render(self.request, 'designer/home.html', context = {'business': business})

    # def get_success_url(self):
        
    #     return super().get_success_url()

class DesignerDetailsView(generic.DetailView):
    model = DesignerRegister
    context_object_name = 'designer'

def designers_home_view(request):
    return render(request, 'designer/designers_home.html')