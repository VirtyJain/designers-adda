from django.views import generic
from django.db import transaction
from django.shortcuts import render, redirect
from .forms import ProductDetailsForm, ProductImageForm
from .models import ProductDetailsModel, ProductImageModel
from designer.models import DesignerRegister
from Home.views import LoginRequiredBaseView


class ProductDetailsView(LoginRequiredBaseView, generic.CreateView):
    
    """
    View to save product details of designers.
    """
    
    form_class = ProductDetailsForm
    template_name = 'products/product_form.html'

    def get(self, request):
        form = ProductDetailsForm()
        return render(request, 'products/product_form.html', {'form': form})

    # TODO use trancsaction.atomic for better performance 
    
    @transaction.atomic
    def post(self, request):
        form = ProductDetailsForm(request.POST)
        images = request.FILES.getlist('image')

        if form.is_valid():
            design = form.save(commit=False)
            designer = DesignerRegister.objects.get(user=request.user)
            design.designer = designer
            design.save()

            # TODO use bulk_create for better performance

            image_list = []
            for image in images:
                image_list.append(ProductImageModel(product=design, product_image=image))
                
            ProductImageModel.objects.bulk_create(image_list)

            return redirect('design_success')

        return render(request, 'products/product_form.html', {'form': form})


# to show success page after product details are saved
def success_url(request):
    return render(request, 'products/success.html')


class ProductListView(generic.ListView):
    
    """
    to show all products in the list view.
    this view is for all users.
    """
    
    template_name = "products/all_products.html"
    model = ProductDetailsModel
    
    
class ProductInfoView(generic.DetailView):
    
    """
    to show product details to the user.
    """
    
    model = ProductDetailsModel
    context_object_name = 'product'
    template_name = 'products/product_info.html'
    
    
class CartProductInfoView(generic.DetailView):
    
    """
    to show cart product details to the user.
    """
    
    model = ProductDetailsModel
    context_object_name = 'product'
    template_name = 'products/cart_product_info.html'