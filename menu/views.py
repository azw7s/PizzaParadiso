from abc import ABC

from django.views import generic
from django.views.generic.edit import FormMixin
from rest_framework import viewsets
from django.urls import reverse_lazy
from .models import MenuCategory, MenuItem, MenuItemOption, OptionValue
from order.models import Cart
from order.forms import CartItemForm
from .serializers import MenuItemSerializer, MenuCategorySerializer, MenuItemOptionSerializer, OptionValueSerializer
from order.serializers import CartItemSerializer
from order.models import CartItem
from customer.models import Customer
from django.shortcuts import redirect
from storages.backends.s3boto3 import S3Boto3Storage
import uuid


# class CustomS3Boto3Storage(S3Boto3Storage, ABC):
#     def get_available_name(self, name, max_length=None):
#         ext = name.split('.')[-1]
#         name = f"{uuid.uuid4()}.{ext}"
#         return super().get_available_name(name, max_length=max_length)
#
#
# class MediaStorage(S3Boto3Storage):
#     location = 'media'
#     file_overwrite = False
#
#
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


def redirect_to_home(request):
    return redirect('/home/')


class Home(generic.TemplateView):
    template_name = 'menu/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['category'] = MenuCategory.objects.all()
        deals = MenuCategory.objects.get(name='deals')
        context['deals'] = MenuItem.objects.filter(category=deals)
        pizza = MenuCategory.objects.get(name='pizza')
        context['pizza'] = MenuItem.objects.filter(category=pizza)

        return context


class MenuCategoryView(viewsets.ModelViewSet):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer


class MenuItemView(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class MenuItemOptionView(viewsets.ModelViewSet):
    queryset = MenuItemOption.objects.all()
    serializer_class = MenuItemOptionSerializer


class OptionValueView(viewsets.ModelViewSet):
    queryset = OptionValue.objects.all()
    serializer_class = OptionValueSerializer


class MenuCategoryDetail(generic.DetailView):
    model = MenuCategory
    template_name = 'menu/menu_category_detail.html'
    context_object_name = 'menu_category'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        category = MenuCategory.objects.get(name=context['menu_category'])
        serialized_category = MenuCategorySerializer(category).data
        context['category'] = serialized_category

        context['categories'] = MenuCategory.objects.all()

        context['url_slug'] = self.kwargs['slug']

        return context


class MenuItemDetail(FormMixin, generic.DetailView):
    model = MenuItem
    form_class = CartItemForm
    template_name = 'menu/menu_item_detail.html'
    context_object_name = 'menu_item'

    def get_form_kwargs(self):
        kwargs = super(MenuItemDetail, self).get_form_kwargs()
        kwargs['menu_item'] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        menu_items = MenuItem.objects.filter(pk=context['menu_item'].pk)
        serialized_items = MenuItemSerializer(menu_items, many=True).data
        context['menu_item'] = serialized_items

        # Serialized Menu Category = SMC
        category = MenuCategory.objects.all()
        serialized_menu = MenuCategorySerializer(category, many=True).data
        context['SMC'] = serialized_menu

        context['categories'] = MenuCategory.objects.all()

        slug = MenuItem.objects.get(slug=self.kwargs['slug'])
        context['url_slug'] = MenuCategory.objects.get(name=slug.category).slug

        return context


# Staff =========================================================================================================

class StaffCreateMenuItem(generic.CreateView):
    model = MenuItem
    fields = ['category', 'image', 'title', 'description', 'price']
    template_name = 'menu/staff_create_menu_item.html'

    def get_success_url(self):
        customer = Customer.objects.get(user=self.request.user)

        return reverse_lazy('staff_view', kwargs={'staff_id': customer.id})


class StaffUpdateMenuItem(generic.UpdateView):
    model = MenuItem
    fields = '__all__'
    template_name = 'menu/staff_update_menu_item.html'
    success_url = reverse_lazy('staff_list_menu_item')

    def get_context_data(self, **kwargs):
        context = super(StaffUpdateMenuItem, self).get_context_data(**kwargs)
        context['menu_item'] = MenuItem.objects.get(pk=self.kwargs['pk'])
        return context


class StaffDeleteMenuItem(generic.DeleteView):
    model = MenuItem
    template_name = 'menu/staff_delete_menu_item.html'
    success_url = reverse_lazy('staff_list_menu_item')


class StaffListMenuItem(generic.ListView):
    model = MenuItem
    template_name = 'menu/staff_list_menu_item.html'
    context_object_name = 'menu_items'































