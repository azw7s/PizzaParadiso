from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

from customer.models import Customer, Address
from menu.models import MenuItem, OptionValue


# Auto-generate
class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid4)

    def __str__(self):
        return self.customer.user.username


# Customer
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_('cart'), related_name="cart_item")
    dish = models.ForeignKey(MenuItem, on_delete=models.CASCADE, blank=False, verbose_name=_('dish'))
    dish_option = models.ManyToManyField(OptionValue, verbose_name=_('dish option'), related_name='dish_option')
    quantity = models.PositiveSmallIntegerField(verbose_name=_("quantity"), default=1)

    def __str__(self):
        return f"{self.dish} : {self.quantity}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('customer'), related_name="order",
                                 null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='order', null=True, blank=True)
    payment_method = models.CharField(_("payment method"), max_length=30)
    delivered = models.BooleanField(_("delivered"), default=False)
    ordered_date = models.DateField(verbose_name=_('ordered date'), auto_now_add=True, null=False)
    total_price = models.DecimalField(_("total price"),
                                      max_digits=5,
                                      decimal_places=3,
                                      validators=[MinValueValidator(0)],
                                      default=0,
                                      )

    def __str__(self):
        return f"{self.customer}, {self.total_price} "


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    item = models.TextField(max_length=50, verbose_name=_('item'))
    quantity = models.PositiveSmallIntegerField(verbose_name=_("quantity"), default=1)
    price = models.DecimalField(_("price"),
                                max_digits=5,
                                decimal_places=3,
                                validators=[MinValueValidator(0)],
                                default=0,
                                )


class OrderItemOption(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='order_item_option')
    item_option = models.TextField(max_length=50, verbose_name=_('item option'), null=True)





















