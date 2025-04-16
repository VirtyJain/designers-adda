from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import login
from .forms import DesignerRegisterForm, DesignerBusinessDetailsForm
from .models import DesignerRegister, DesignerBusinessDetails
from Home.forms import CustomerChangeForm
from products.models import ProductDetailsModel
from products.forms import ProductDetailsForm
from orders.models import OrderModel
from Home.views import LoginRequiredBaseView
# Create your views here.


def about(request):
    return render(request, template_name="designer/about.html")


def designers_home_view(request):
    
    designer = DesignerRegister.objects.get(user=request.user)  # Assuming a related Designer model
    designer_id = designer.id
    
    orders = OrderModel.objects.filter(
        cart_product__product__designer=designer
    ).select_related('user', 'cart_product__product')

    return render(request, 'designer/designers_home.html', {
        'designer': designer,
        'designer_id': designer_id,
        'orders': orders,
    })


class DesignerFormView(LoginRequiredBaseView, generic.FormView):
    
    """
    View to save designer details.
    """
    
    form_class = DesignerRegisterForm
    template_name = 'designer/designer_register.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user # Passing the current user to the form
        return kwargs

    def form_valid(self, form):
        user = self.request.user

        user.user_type = 'Designer'
        user.save(update_fields=['user_type'])
        login(self.request, user)
        user.save()
        
        # Saving the designer details
        designer = form.save(commit=False)
        designer.user = user
        designer.save()
        

        # Redirect to business details form, pass designer.pk in session
        self.request.session['designer_id'] = designer.pk
        return redirect('designer_business_register', pk=designer.pk)


class DesignerBusinessFormView(LoginRequiredBaseView, generic.CreateView):
    
    """
    View to save designer business details.
    """
    
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


class DesignerDetailsView(LoginRequiredBaseView, generic.DetailView):
    
    """
    view to display designer profile.
    """
    
    model = DesignerRegister
    context_object_name = 'designer'
    template_name = 'designer/designer_detail.html'


class DesignerDetailUpdateView(LoginRequiredBaseView, generic.View):
    
    """
    view to update designer profile.
    """
    
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
    
    """
    view to list all designer's profile.
    """
    
    template_name = "designer/all_designers.html"
    model = DesignerRegister
    
    
class DesignerInfoView(generic.DetailView):
    
    """
    view to display designer profile to customer.
    """
    
    model = DesignerRegister
    context_object_name = 'designer'
    template_name = 'designer/designer_info.html'
    
    
class DesignerProductListView(LoginRequiredBaseView, generic.ListView):
    
    """
    view to display designer's all products.
    """
    
    template_name = "designer/designer_products.html"
    model = ProductDetailsModel
    
    def get_queryset(self):
        designer_id = self.kwargs['pk']
        return ProductDetailsModel.objects.filter(designer=designer_id)
    
   
class DesignerProductInfoView(LoginRequiredBaseView, generic.DetailView):
    
    """
    view to display designer's all product's detail.
    """
    
    model = ProductDetailsModel
    context_object_name = 'product'
    template_name = 'designer/product_info.html'
    

class DesignerProductUpdateView(LoginRequiredBaseView, generic.UpdateView):
    
    """
    view to update designer's product details.
    """
    
    model = ProductDetailsModel
    form_class = ProductDetailsForm
    template_name = "designer/product_update.html"
    
    def get_success_url(self):
        return reverse('designer_products', kwargs={'pk': self.object.designer.pk})
    

class DesignerProductDeleteView(LoginRequiredBaseView, generic.DeleteView):
    
    """
    view to delete designer's product.
    """
    
    model = ProductDetailsModel
    template_name = "designer/product_delete.html"

    def get_success_url(self):
        return reverse('designer_products', kwargs={'pk': self.object.designer.pk})


class ViewDesignersOrder(LoginRequiredBaseView, generic.ListView):
    
    """
    view to display designer's all orders.
    """
    
    template_name = "designer/designers_home.html"
    model = OrderModel
    context_object_name = 'orders'
    
    def get_queryset(self):
        designer_id = self.kwargs['pk']
        return OrderModel.objects.filter(
            cart_product__product__designer_id=designer_id
        ).select_related('user', 'cart_product__product')