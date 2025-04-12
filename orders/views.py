from django.shortcuts import render, redirect, get_object_or_404
from products.models import ProductDetailsModel
from .models import CartModel


def add_to_cart(request, pk):
    product = get_object_or_404(ProductDetailsModel, id=pk)
    cart_item, created = CartModel.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.save()
    return redirect('view_cart', pk=request.user.pk)


def view_cart(request, pk):
    cart_items = CartModel.objects.filter(user=request.user)
    return render(request, 'orders/cart.html', {'cart_items': cart_items, pk:pk})
