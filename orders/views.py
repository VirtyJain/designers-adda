from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
from django.conf import settings
from django.views import generic
from products.models import ProductDetailsModel
from .models import CartModel, OrderModel
from delivery_boy.models import DeliveryBoyModel
from Home.views import LoginRequiredBaseView


# to add product to cart
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(ProductDetailsModel, id=pk)
    cart_item, created = CartModel.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.save()
    return redirect('view_cart', pk=request.user.pk)


# to view cart
@login_required
def view_cart(request, pk):
    cart_items = CartModel.objects.filter(user=request.user)
    return render(request, 'orders/cart.html', {'cart_items': cart_items, pk:pk})


# to place order
@login_required
def place_order(request, pk):
    cart_item = get_object_or_404(CartModel, id=pk, user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        house_no = request.POST.get('house_no')
        address = request.POST.get('address')
        landmark = request.POST.get('landmark', '')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        user = request.user
        total_price = cart_item.product.product_price * quantity

        delivery_boys = list(DeliveryBoyModel.objects.all())
        delivery_boy = random.choice(delivery_boys) if delivery_boys else None

        order = OrderModel.objects.create(
            cart_product=cart_item,
            user=user,
            quantity=quantity,
            total_price=total_price,
            delivery_boy=delivery_boy,
            house_no=house_no,
            address=address,
            landmark=landmark,
            city=city,
            state=state,
            pincode=pincode
        )


        # Email to Customer
        send_mail(
            subject = 'Welcome to Designer’s Adda!',
            message = f'{user.first_name}, Your Order Placed Successfully. Thank you for Shopping with us.\n\nYour order will be delivered to you soon.\n\n Continue Shopping....',
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [user.email],
            fail_silently = False,
        )

        # Email to Delivery Boy
        if delivery_boy:
            send_mail(
                subject='New Order Assigned',
                message=f'Dear {delivery_boy.user.first_name}, a new order has been assigned to you.\nDeliver to: { order.house_no }, {order.address}, {order.landmark}, {order.city}, {order.state}, {order.pincode}. \n \nOrder Details:\nProduct: {cart_item.product.product_name}\nQuantity: {quantity}\nTotal Price: {total_price}. \n Pick this product from designer: {cart_item.product.designer.user.first_name} {cart_item.product.designer.user.last_name}.\n Contact: {cart_item.product.designer.user.contact_no}.\n\n Thankyou.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[delivery_boy.user.email],
                fail_silently=False,
            )

        # Email to Designer
        designer = cart_item.product.designer
        send_mail(
            subject='Your Product Got Ordered!',
            message=f'Hi {designer.user.first_name}, your product "{cart_item.product.product_name}" has been ordered by {user}. Make sure to prepare it for delivery.\n\nOrder Details:\nQuantity: {quantity}\nTotal Price: {total_price} \n\n The delivery boy will reach out to you soon. \n\n Thankyou.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[designer.user.email],
            fail_silently=False,
        )

        return redirect('order_success')

    return render(request, 'orders/place_order.html', {'cart_item': cart_item})


# to show order success page
@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')


# to view order history
@login_required
def order_history(request, pk):
    order_items = OrderModel.objects.filter(user=request.user)
    return render(request, 'orders/orders.html', {'order_items': order_items, pk:pk})


class OrderProductInfoView(LoginRequiredBaseView, generic.DetailView):
    
    """
    View to display ordered product details.
    """
    model = OrderModel
    context_object_name = 'order_product'
    template_name = 'orders/product_order_detail.html'