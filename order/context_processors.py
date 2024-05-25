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
            cart = Cart.objects.get(customer=customer)
            cart_id = cart.id

        except Customer.DoesNotExist:
            return {'error_message': 'Customer does not exist'}
        except Cart.DoesNotExist:
            return {'error_message': 'Cart does not exist'}

    return {'cart_id': cart_id}


def get_cart_item_count(request):
    cart_item_count = None
    if request.user.is_authenticated:
        user = request.user
        try:
            cart = Cart.objects.get(customer=Customer.objects.get(user=user))
            cart_item = CartItem.objects.filter(cart=cart)
            cart_item_count = cart_item.count()

        except Customer.DoesNotExist:
            return {'error_message': 'Customer does not exist'}
        except Cart.DoesNotExist:
            return {'error_message': 'Cart does not exist'}

    return {'cart_item_count': cart_item_count}




