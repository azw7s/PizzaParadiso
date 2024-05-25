from django import forms
from django.utils.text import slugify
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.models import User
from .models import Customer, Address


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'user']
