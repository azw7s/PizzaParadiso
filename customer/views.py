from django.shortcuts import render, redirect
from django.views import generic
from .forms import CustomerForm, CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from .models import Customer, Address
from order.models import Cart, Order
from .serializers import AddressSerializer


class SignUpView(UserPassesTestMixin, generic.edit.CreateView):
    template_name = 'customer/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()

        # Create a Customer acc for user
        phone_number = self.request.POST.get('phone_number')
        customer = Customer.objects.create(user=user, phone_number=phone_number)

        # Create a Cart for Customer
        Cart.objects.create(customer=customer)

        return redirect(self.success_url)

    def test_func(self):
        # Allow access only if the user is not logged in
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('menu_list')


class CustomLogin(LoginView):

    def get_success_url(self):
        next_page = self.request.POST.get('next_page')

        if next_page:
            return next_page
        else:
            return super().get_success_url()


# Customer ---------------------------------------------------------------------------------------------------------

class UserUpdate(generic.UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'customer/user_update.html'
    slug_field = 'customer'
    slug_url_kwarg = 'customer'

    def get_success_url(self):
        customer = Customer.objects.get(user=self.request.user)
        return reverse_lazy('customer_detail', kwargs={'customer_id': customer.id})

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)

        context['customer'] = Customer.objects.get(user=self.request.user)

        return context


class CustomerDetail(LoginRequiredMixin, generic.DetailView):
    model = Customer
    template_name = 'customer/customer_detail.html'
    context_object_name = 'customer'
    slug_field = 'uuid'
    slug_url_kwarg = 'customer_uuid'


# Address --------------------------------------------------------------------------------------------------------------


class AddressCreate(generic.CreateView):
    model = Address
    fields = ['customer', 'state', 'city', 'block', 'street', 'road', 'building', 'floor',
              'apartment', 'address_description', 'phone_number', 'active']
    template_name = 'customer/address_create.html'

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(AddressCreate, self).get_context_data(**kwargs)

        context['customer'] = Customer.objects.get(user=self.request.user)
        return context


class AddressUpdate(generic.UpdateView):
    model = Address
    fields = ['state', 'city', 'block', 'street', 'road', 'building', 'floor',
              'apartment', 'address_description', 'phone_number', 'active']
    template_name = 'customer/address_update.html'
    context_object_name = 'address'

    def get_success_url(self):
        next_url = self.request.POST.get('next')

        if next_url:
            return next_url
        else:
            return reverse_lazy('home')


class AddressList(generic.ListView):
    model = Address
    template_name = 'customer/address_list.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        address = Address.objects.filter(customer=customer)
        return address

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AddressList, self).get_context_data(**kwargs)

        return context


class AddressCheckoutList(generic.ListView):
    model = Address
    template_name = 'customer/address_checkout_list.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        address = Address.objects.filter(customer=customer)
        return address


class AddressDelete(generic.DeleteView):
    model = Address
    template_name = 'customer/address_delete.html'

    def get_success_url(self):

        customer = Customer.objects.get(user=self.request.user)
        return reverse_lazy('address_list', kwargs={'customer_id': customer.id})


# Staff =================================================================================================

class StaffView(generic.TemplateView):
    template_name = 'customer/staff_view.html'
    slug_field = 'staff'
    slug_url_kwarg = 'staff_uuid'

    def get_context_data(self, **kwargs):
        context = super(StaffView, self).get_context_data(**kwargs)

        return context















