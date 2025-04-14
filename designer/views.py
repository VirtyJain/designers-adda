from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from .forms import DesignerRegisterForm, DesignerBusinessDetailsForm
from .models import DesignerRegister, DesignerBusinessDetails
from Home.forms import CustomerChangeForm
from products.models import ProductDetailsModel
from products.forms import ProductDetailsForm
# Create your views here.


def about(request):
    return render(request, template_name="designer/about.html")


def designers_home_view(request):
    
    designer = DesignerRegister.objects.get(user=request.user)  # Assuming a related Designer model
    designer_id = designer.id
    
    return render(request, 'designer/designers_home.html', {
        'designer': designer,
        'designer_id': designer_id,
    })


class DesignerFormView(generic.FormView):
    form_class = DesignerRegisterForm
    template_name = 'designer/designer_register.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user # Passing the current user to the form
        return kwargs

    def form_valid(self, form):
        user = self.request.user

        user.user_type = 'designer'
        user.save()
        
        # Saving the designer details
        designer = form.save(commit=False)
        designer.user = user
        designer.save()

        # Redirect to business details form, pass designer.pk in session
        self.request.session['designer_id'] = designer.pk
        return redirect('designer_business_register', pk=designer.pk)


class DesignerBusinessFormView(generic.CreateView):
    form_class = DesignerBusinessDetailsForm
    template_name = 'designer/business_details.html'

    def dispatch(self, request, *args, **kwargs):
        
        # getting the designer from session
        self.designer_id = request.session.get('designer_id')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        designer = get_object_or_404(DesignerRegister, pk=self.designer_id)
        business = form.save(commit=False)
        business.designer = designer
        business.save()

        # Clean up session
        del self.request.session['designer_id']

        return redirect('designer_home_page')


class DesignerDetailsView(generic.DetailView):
    model = DesignerRegister
    context_object_name = 'designer'
    template_name = 'designer/designer_detail.html'


class DesignerDetailUpdateView(generic.View):
    
    def get(self, request, pk):
        
        business = get_object_or_404(DesignerBusinessDetails, pk=pk)
        designer_form = DesignerRegisterForm(instance=business.designer)
        user_form = CustomerChangeForm(instance=business.designer.user)
        business_form = DesignerBusinessDetailsForm(instance=business)
        
        return render(request, 'designer/designer_update_form.html', {
            'business': business_form,
            'user': user_form,
            'designer':designer_form,
        })
        
    def post(self, request, pk):
        
        business = get_object_or_404(DesignerBusinessDetails, pk=pk)
        designer_form = DesignerRegisterForm(request.POST, instance=business.designer)
        user_form = CustomerChangeForm(request.POST, instance=business.designer.user)
        business_form = DesignerBusinessDetailsForm(request.POST, instance=business)
        
        if designer_form.is_valid() and user_form.is_valid() and business_form.is_valid():
            designer = designer_form.save()
            user_form.save()
            business_form.save()
            
            return redirect('designer_details', pk=designer.pk)
        
        return render(request, 'designer/designer_update_form.html', {
            'business': business_form,
            'user': user_form,
            'designer':designer_form,
        })


class DesignerListView(generic.ListView):
    template_name = "designer/all_designers.html"
    model = DesignerRegister
    
    
class DesignerInfoView(generic.DetailView):
    model = DesignerRegister
    context_object_name = 'designer'
    template_name = 'designer/designer_info.html'
    
    
class DesignerProductListView(generic.ListView):
    template_name = "designer/designer_products.html"
    model = ProductDetailsModel
    
    def get_queryset(self):
        designer_id = self.kwargs['pk']
        return ProductDetailsModel.objects.filter(designer=designer_id)
    
   
class DesignerProductInfoView(generic.DetailView):
    model = ProductDetailsModel
    context_object_name = 'product'
    template_name = 'designer/product_info.html'
    

class DesignerProductUpdateView(generic.UpdateView):
    model = ProductDetailsModel
    form_class = ProductDetailsForm
    template_name = "designer/product_update.html"
    
    def get_success_url(self):
        return reverse('designer_products', kwargs={'pk': self.object.designer.pk})
    

class DesignerProductDeleteView(generic.DeleteView):
    model = ProductDetailsModel
    template_name = "designer/product_delete.html"

    def get_success_url(self):
        return reverse('designer_products', kwargs={'pk': self.object.designer.pk})
