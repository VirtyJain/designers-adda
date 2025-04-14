from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from products.models import ProductDetailsModel
from .models import CartModel, OrderModel


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(ProductDetailsModel, id=pk)
    cart_item, created = CartModel.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.save()
    return redirect('view_cart', pk=request.user.pk)


@login_required
def view_cart(request, pk):
    cart_items = CartModel.objects.filter(user=request.user)
    return render(request, 'orders/cart.html', {'cart_items': cart_items, pk:pk})


@login_required
def place_order(request, pk):
    cart_item = get_object_or_404(CartModel, id=pk, user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        user = request.user
        total_price = cart_item.product.product_price * quantity

        order = OrderModel.objects.create(
            cart_product=cart_item,
            user=user,
            quantity=quantity,
            total_price=total_price,
        )
        
        send_mail(
            subject = 'Welcome to Designer’s Adda!',
            message = f'{user.first_name}, Your Order Placed Successfully. Thank you for Shopping with us.\n\nYour order will be delivered to you soon.\n\n Continue Shopping....',
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [user.email],
            fail_silently = False,
        )
        
        return redirect('order_success')

    return render(request, 'orders/place_order.html', {'cart_item': cart_item})


def order_success(request):
    return render(request, 'orders/order_success.html')


@login_required
def order_history(request, pk):
    order_items = OrderModel.objects.filter(user=request.user)
    return render(request, 'orders/orders.html', {'order_items': order_items, pk:pk})