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
<<<<<<< HEAD
        customer = Customer.objects.get(user=user)
        cart = Cart.objects.get(customer)
        cart_item = CartItem.objects.filter(cart=cart)

        try:
            cart_item_count = cart_item.count()

        except user.DoesNotExist:
            return {'error_message': 'user does not exist'}
        except customer.DoesNotExist:
            return {'error_message': 'Customer does not exist'}
        except cart.DoesNotExist:
            return {'error_message': 'Cart does not exist'}
        except cart_item.DoesNotExist:
            return {'error_message': 'CartItem does not exist'}
=======
        try:
            cart = Cart.objects.get(customer=Customer.objects.get(user=user))
            cart_item = CartItem.objects.filter(cart=cart)
            cart_item_count = cart_item.count()

        except Customer.DoesNotExist:
            return {'error_message': 'Customer does not exist'}
        except Cart.DoesNotExist:
            return {'error_message': 'Cart does not exist'}
>>>>>>> 5d4a96d70fe3dcf780b3a5ff1d887c2282ee880e

    return {'cart_item_count': cart_item_count}



<<<<<<< HEAD
=======

>>>>>>> 5d4a96d70fe3dcf780b3a5ff1d887c2282ee880e
