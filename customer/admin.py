from django.contrib import admin
from .models import Customer, Address


class CustomerAdmin(admin.ModelAdmin):
    model = Customer


class AddressAdmin(admin.ModelAdmin):
    model = Address


admin.site.register(Address)
admin.site.register(Customer)
