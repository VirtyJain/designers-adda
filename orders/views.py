import random

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.views import View, generic
from django.views.decorators.csrf import csrf_exempt

from delivery_boy.models import DeliveryBoyModel
from Home.views import LoginRequiredBaseView
from products.models import ProductDetailsModel

from .models import CartModel, OrderModel, PaymentModel


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
        total_price = (cart_item.product.product_price * quantity) + 50 # delivery charge 

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
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': cart_item.product.product_name,
                        },
                        'unit_amount': int(total_price * 100),
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('payment_success')),
            cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
        )
        
        PaymentModel.objects.create(
            order=order,
            stripe_payment_intent=checkout_session.payment_intent,
            stripe_checkout_session_id=checkout_session.id,
        )
        
        return redirect(checkout_session.url)

    return render(request, 'orders/place_order.html', {'cart_item': cart_item})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session['customer_email']['email']
        payment_intent = session['payment_intent']
        
        payment = PaymentModel.objects.get(stripe_payment_intent=payment_intent)
        order = payment.order
        
        payment.payment_status = 'Completed'
        payment.save()
        order.order_status = 'Processing'
        order.save()

        user = order.user
        product = order.cart_product.product
        designer = product.designer.user
        delivery_boy = order.delivery_boy.user

        context = {
            "user_name": user.first_name,
            "product_name": product.product_name,
            "quantity": order.quantity,
            "total_price": order.total_price,
            "delivery_boy": delivery_boy.first_name,
            "house_no": order.house_no,
            "address": order.address,
            "landmark": order.landmark,
            "city": order.city,
            "state": order.state,
            "pincode": order.pincode,
            "designer_name": f'{designer.first_name} {designer.last_name}',
            "designer_contact": designer.contact_no,
        }

        # Email to Customer
        receiver_email = user.email
        template_name = "orders/customer_email.html"
        convert_to_html_content =  render_to_string(
            template_name=template_name,
            context=context
        )
        plain_message = strip_tags(convert_to_html_content)

        send_mail(
            subject="Order Placed Successfully",
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[receiver_email,],
            html_message=convert_to_html_content,
            fail_silently=True
        )
        
        # Email to Designer
        receiver_email = order.cart_item.product.designer.user.email
        template_name = "orders/designer_email.html"
        convert_to_html_content =  render_to_string(
            template_name=template_name,
            context=context
        )
        plain_message = strip_tags(convert_to_html_content)

        send_mail(
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

        send_mail(
            subject="New Order Received",
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[receiver_email,],
            html_message=convert_to_html_content,
            fail_silently=True
        )    
        return render(request, 'orders/payment_success.html')

    return HttpResponse(status=200)


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


def payment_success(request):
    return render(request, 'orders/payment_success.html')
    

def payment_cancel(request):
    return render(request, 'orders/payment_cancel.html')