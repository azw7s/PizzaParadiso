from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem, OrderItemOption

from customer.serializers import CustomerSerializer, AddressSerializer
from menu.serializers import MenuItemSerializer, OptionValueSerializer
from menu.models import OptionValue


class CartItemSerializer(serializers.ModelSerializer):
    dish = MenuItemSerializer()
    dish_option = OptionValueSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem,):
        main_price = cart_item.dish.price
        if cart_item.dish_option.exists():
            option_prices = [option.price for option in cart_item.dish_option.all() if option.price is not None]
            if option_prices:
                main_price = max(option_prices)

        return main_price * cart_item.quantity

    class Meta:
        model = CartItem
        fields = ['pk', 'cart', 'dish', 'dish_option', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    cart_item = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    customer = CustomerSerializer()

    def get_total_price(self, cart):
        main_price = 0

        for item in cart.cart_item.all():
            if item.dish_option.exists():
                option_prices = [option.price for option in item.dish_option.all() if option.price is not None]
                if option_prices:
                    main_price += max(option_prices) * item.quantity
            else:
                main_price += item.quantity * item.dish.price

        return main_price

    class Meta:
        model = Cart
        fields = ['customer', 'id', 'cart_item', 'total_price']


class OrderItemOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItemOption
        fields = ['order_item', 'item_option']


class OrderItemSerializer(serializers.ModelSerializer):
    order_item_option = OrderItemOptionSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = ['order', 'item', 'quantity', 'price', 'order_item_option']


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True)
    customer = CustomerSerializer()
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = ['pk', 'customer', 'address', 'payment_method', 'delivered',
                  'ordered_date', 'total_price', 'order_item']


