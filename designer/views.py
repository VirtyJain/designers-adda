from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .forms import DesignerRegisterForm, DesignerBusinessDetailsForm
from .models import DesignerRegister, DesignerBusinessDetails
from Home.forms import CustomerForm
# Create your views here.


def about(request):
    return render(request, template_name="designer/about.html")


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
    template_name = 'designer/designer_detail.html'
    
    # def get_context_data(self, **kwargs):
    #     print(kwargs)
    #     breakpoint()
    #     return super().get_context_data(**kwargs)

def designers_home_view(request):
    return render(request, 'designer/designers_home.html')


class DesignerUpdateView(generic.UpdateView):
    model = DesignerRegister
    fields = ['__all__']
    success_url = '/designer/profile/'


class DesignerDetailUpdateView(generic.View):
    
    def get(self, request, pk):
        
        business = get_object_or_404(DesignerBusinessDetails, pk=pk)
        designer_form = DesignerRegisterForm(instance=business.designer)
        user_form = CustomerForm(instance=business.designer.user)
        business_form = DesignerBusinessDetailsForm(instance=business)
        
        return render(request, 'designer/designerregister_form.html', {
            'business': business_form,
            'user': user_form,
            'designer':designer_form,
        })
        
    def post(self, request, pk):
        business = get_object_or_404(DesignerBusinessDetails, pk=pk)
        designer_form = DesignerRegisterForm(request.post, instance=business.designer)
        user_form = CustomerForm(request.post, instance=business.designer.user)
        business_form = DesignerBusinessDetailsForm(request.post, instance=business)
        
        if designer_form.is_valid() and user_form.is_valid() and business_form.is_valid():
            designer_form.save()
            user_form.save()
            business_form.save()
            
            return redirect('designer_details')
        
        return render(request, 'designer/designerregister_form.html', {
            'business': business_form,
            'user': user_form,
            'designer':designer_form,
        })
