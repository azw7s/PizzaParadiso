from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib import messages
from order.models import Cart, CartItem
from customer.models import Customer


def get_cart_id(request):
    cart_id = None
    if request.user.is_authenticated:
        user = request.user
        try:
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=user, phone_number='+96550669593')

        try:
            cart = Cart.objects.get(customer=customer)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(customer=customer)

        cart_id = cart.id

    return {'cart_id': cart_id}


def get_cart_item_count(request):
    cart_item_count = None
    if request.user.is_authenticated:
        user = request.user

        try:
            customer = Customer.objects.get(user=user)
            cart = Cart.objects.get(customer=customer)
            cart_item = CartItem.objects.filter(cart=cart)
            cart_item_count = cart_item.count()

        except Cart.DoesNotExist or Customer.DoesNotExist:
            return {'error': 'cart does not exist'}

    return {'cart_item_count': cart_item_count}