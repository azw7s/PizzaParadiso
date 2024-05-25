from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, OrderItemOption


class CartItemAdmin(admin.ModelAdmin):
    model = CartItem


class CartAdmin(admin.ModelAdmin):
    model = Cart


class OrderAdmin(admin.ModelAdmin):
    model = Order


class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem


class OrderItemOptionAdmin(admin.ModelAdmin):
    model = OrderItemOption


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderItemOption, OrderItemOptionAdmin)