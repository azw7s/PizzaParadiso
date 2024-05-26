from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from phonenumber_field.modelfields import PhoneNumberField
from autoslug import AutoSlugField


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')
    slug = AutoSlugField(populate_from="user", unique=True, blank=False, null=False)
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    phone_number = PhoneNumberField(_('phone number'), unique=True, blank=False)
    created_date = models.DateTimeField(_('created date'), auto_now_add=True)

    def __str__(self):
        return f'customer : {self.user.username}'


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='address')
    phone_number = PhoneNumberField(_('phone number'), blank=False)
    state = models.CharField(_('state'), max_length=50)
    city = models.CharField(_('city'), max_length=50,)
    block = models.PositiveSmallIntegerField(_('block'),)
    street = models.CharField(_('street'), max_length=50)
    road = models.CharField(_('road'), max_length=30, blank=True, null=True)
    building = models.CharField(_('building'), max_length=30)
    floor = models.PositiveSmallIntegerField(_('floor'), null=True)
    apartment = models.PositiveSmallIntegerField(_('apartment'))
    address_description = models.TextField(_('address description'), null=True, blank=True)
    active = models.BooleanField(_('active'), default=False)

    def __str__(self):
        return f"{self.state}, {self.city}, block {self.street}"

    def save(self, *args, **kwargs):
        # Check if the address is being activated
        if self.active:
            # Deactivate all other addresses for the same customer
            Address.objects.filter(customer=self.customer).exclude(pk=self.pk).update(active=False)
        super().save(*args, **kwargs)



