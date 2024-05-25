from django import forms
from .models import CartItem, Order
from menu.models import OptionValue


class CartItemForm(forms.Form):

    def __init__(self, *args, **kwargs):
        menu_item = kwargs.pop('menu_item')
        super(CartItemForm, self).__init__(*args, **kwargs)
        option_groups = menu_item.menu_item_option.all()

        for option_group in option_groups:
            option_values = option_group.option_value.all()
            choices = [(option_value.id, str(option_value)) for option_value in option_values]

            self.fields[f'dish_option_{option_group.id}'] = forms.ChoiceField(
                label=option_group.field_name,
                choices=choices,
                widget=forms.RadioSelect,
                required=True
            )

    class Meta:
        model = CartItem
        fields = ['cart', 'dish', 'dish_option', 'quantity']


class OrderForm(forms.Form):
    class Meta:
        model = Order
        fields = ['item', 'address', 'payment_method', 'total_price']
