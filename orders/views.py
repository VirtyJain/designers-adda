from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
        
        context = {
            "user_name": user.first_name,
            "product_name": cart_item.product.product_name,
            "quantity": quantity,
            "total_price": total_price,
            "delivery_boy": delivery_boy.user.first_name,
            "house_no": house_no,
            "address": address,
            "landmark": landmark,
            "city": city,
            "state": state,
            "pincode": pincode,
            "designer_name": f'{ cart_item.product.designer.user.first_name } { cart_item.product.designer.user.last_name }',
            "designer_contact": cart_item.product.designer.user.contact_no,
            
        }

        # Email to Customer
        receiver_email = user.email
        template_name = "orders/customer_email.html"
        convert_to_html_content =  render_to_string(
            template_name=template_name,
            context=context
        )
        plain_message = strip_tags(convert_to_html_content)

        yo_send_it = send_mail(
            subject="Order Placed Successfully",
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[receiver_email,],
            html_message=convert_to_html_content,
            fail_silently=True
        )
        
        # Email to Designer
        receiver_email = cart_item.product.designer.user.email
        template_name = "orders/designer_email.html"
        convert_to_html_content =  render_to_string(
            template_name=template_name,
            context=context
        )
        plain_message = strip_tags(convert_to_html_content)

        yo_send_it = send_mail(
            subject="New Order Received",
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[receiver_email,],
            html_message=convert_to_html_content,
            fail_silently=True
        )
        
        # Email to Delivery boy
        receiver_email = delivery_boy.user.email
        template_name = "orders/delivery_boy_email.html"
        convert_to_html_content =  render_to_string(
            template_name=template_name,
            context=context
        )
        plain_message = strip_tags(convert_to_html_content)

        yo_send_it = send_mail(
            subject="New Order Received",
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[receiver_email,],
            html_message=convert_to_html_content,
            fail_silently=True
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