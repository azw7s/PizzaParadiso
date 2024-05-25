from django.views import View
from rest_framework import viewsets
from django.views import generic
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, reverse, render
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from aa_pizza.settings import YOUR_DOMAIN, STRIPE_PUBLIC_KEY
from django.conf import settings
from django.http import HttpResponseRedirect
import stripe
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer
from .forms import CartItemForm, OrderForm
from .models import Cart, CartItem, Order, OrderItem, OrderItemOption
from customer.models import Customer, Address
from menu.models import MenuItem, OptionValue, MenuCategory, MenuItemOption


# Checkout and Payment ------------------------------------------------------------------------------------------------

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderPlaced(generic.TemplateView):
    template_name = 'order/order_placed.html'

    def get_context_data(self, **kwargs):
        context = super(OrderPlaced, self).get_context_data(**kwargs)

        customer = Customer.objects.get(user=self.request.user)
        cart = Cart.objects.get(customer=customer)
        cart_item = CartItem.objects.filter(cart=cart)

        context['customer'] = customer
        context['cart'] = CartSerializer(cart).data
        context['address'] = Address.objects.get(customer=customer, active=True)

        referer = self.request.META.get('HTTP_REFERER')
        if referer is None:
            context['payment_method'] = 'card'
        elif referer or referer.endswith('/checkout/'):
            context['payment_method'] = 'cash'

        return context


class PaymentFailed(generic.TemplateView):
    template_name = 'order/payment_failed.html'


class CreateCheckoutSession(View):

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(id=self.kwargs['cart_id'])
        cart_items = CartItem.objects.filter(cart=cart).values_list('dish__title', flat=True)
        cart_items_title = str(list(cart_items))
        cart_serializer = CartSerializer(cart)
        cart_total_price = int(cart_serializer.data['total_price'] * 1000)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'kwd',
                        'unit_amount': cart_total_price,
                        'product_data': {
                            'name': 'Pizza Paradiso',
                            'description': cart_items_title,
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": cart.pk
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/order/placed/',
            cancel_url=YOUR_DOMAIN + '/payment/failed/',
        )

        return JsonResponse({
                'id': checkout_session.id
        })


class Checkout(generic.TemplateView):
    template_name = 'order/checkout.html'

    def get_context_data(self, **kwargs):
        context = super(Checkout, self).get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        cart = Cart.objects.get(customer=customer)
        cart_serializer = CartSerializer(cart).data
        context.update({
            'cart': cart,
            'SMC': cart_serializer,
            'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY,
            'address': Address.objects.get(customer=customer, active=True)
        })
        return context


# Cart --------------------------------------------------------------------------------------------------------


@require_POST
def update_cart_item_quantity(request):
    if request.method == 'POST':
        operation = request.POST.get('operation')
        cart_item_pk = request.POST.get('cart_item_pk')
        try:
            cart_item = CartItem.objects.get(pk=cart_item_pk)
            cart_id = cart_item.cart.id
            if operation == '+':
                cart_item.quantity += 1
            elif operation == '-':
                cart_item.quantity -= 1

            cart_item.save()

            if cart_item.quantity < 1:
                cart_item.delete()
            return redirect('cart_detail', cart_id=cart_id)
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message':   'Cart item not found'})


class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemView(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


# Adding items to Cart
class CartItemCreate(generic.CreateView):
    model = CartItem
    fields = ['cart', 'dish', 'dish_option', 'quantity']
    template_name = 'order/cart_item_create.html'

    def get_success_url(self, *args, **kwargs):
        if self.request.method == 'POST':
            category = MenuCategory.objects.get(pk=self.request.POST.get('category'))
            return reverse_lazy('menu', kwargs={'slug': category.slug})
        else:
            return reverse_lazy('menu', kwargs={'slug': 'pizza'})

    def form_valid(self, form):

        selected_dish_options = [value for field_name, value in self.request.POST.items()
                                 if field_name.startswith('dish_option_')]

        form.cleaned_data['dish_option'] = selected_dish_options

        cart = form.cleaned_data['cart']
        dish = form.cleaned_data['dish']

        dish_options = []
        for option in selected_dish_options:
            option_value = OptionValue.objects.get(pk=option)
            dish_options.append(option_value)

        # check if the cart, dish and all dish_options are exactly the same thing
        matching_item = None
        for item in CartItem.objects.filter(cart=cart, dish=dish):
            if set(item.dish_option.all()) == set(dish_options):
                matching_item = item
                break

        # if they are same +1 the quantity
        if matching_item:
            matching_item.quantity += form.cleaned_data['quantity']
            matching_item.save()
            return HttpResponseRedirect(self.get_success_url())

        # if they are different create a new cart item
        else:
            new_cart_item = form.save()
            return super().form_valid(form)


class CartDetail(LoginRequiredMixin, generic.DetailView):
    model = Cart
    template_name = 'order/cart_detail.html'

    # use id field in url path
    slug_field = 'id'
    slug_url_kwarg = 'cart_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch data using the DRF viewset
        cart = self.object

        # Serialize cart details
        cart_serializer = CartSerializer(cart)
        context['cart_view'] = cart_serializer.data

        # Serialize related cart items
        cart_items = CartItem.objects.filter(cart=cart)
        cart_item_serializer = CartItemSerializer(cart_items, many=True)
        context['cart_item_view'] = cart_item_serializer.data

        context['address'] = Address.objects.filter(customer=Customer.objects.get(user=self.request.user))

        return context


# Order -----------------------------------------------------------------------------------------------


def order_delivered_update(request):
    if request.method == 'POST':
        order_pk = request.POST.get('order_pk')
        order = Order.objects.get(pk=order_pk)
        order.delivered = True
        order.save()
        return redirect(reverse('order_staff', kwargs={'staff_id': request.user.customer.id}))


class OrderCreate(generic.CreateView):
    model = Order
    fields = '__all__'
    template_name = 'order/order_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        order = form.save()

        customer = Customer.objects.get(user=self.request.user)
        cart = Cart.objects.get(customer=customer)
        cart_items = CartItem.objects.filter(cart=cart)

        for cart_item in cart_items:
            cart_item_serializer = CartItemSerializer()
            total_price = cart_item_serializer.get_total_price(cart_item)
            order_item = OrderItem.objects.create(order=order, item=cart_item.dish.title, quantity=cart_item.quantity,
                                                  price=total_price)

            dish_option = cart_item.dish_option.all()

            for option in dish_option:
                OrderItemOption.objects.create(order_item=order_item, item_option=option.value)

            cart_items.delete()

        return super().form_valid(form)


class OrderList(generic.ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderList, self).get_context_data(**kwargs)

        customer = Customer.objects.get(user=self.request.user)
        order = Order.objects.filter(customer=customer)
        serialized_order = OrderSerializer(order, many=True)

        context['orders'] = serialized_order.data
        context['customer'] = customer

        return context


#  Staff ==============================================================================================================

class OrderStaff(generic.ListView):
    model = Order
    template_name = 'order/order_staff.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super(OrderStaff, self).get_queryset()

        today_date = timezone.now().date()
        order = Order.objects.filter(ordered_date=today_date, delivered=False)
        queryset = OrderSerializer(order, many=True).data

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderStaff, self).get_context_data(**kwargs)

        context['cart_item'] = CartItem.objects.filter()

        return context














