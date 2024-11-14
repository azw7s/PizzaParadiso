from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from autoslug import AutoSlugField


# Employee
class MenuCategory(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')
    image = models.ImageField(_('Image'), upload_to='images/', null=True)
    name = models.CharField(_('name'), max_length=30, unique=True, blank=False)
    slug = AutoSlugField(populate_from="name", unique=True, null=False)

    def __str__(self):
        return self.name


# Employee
class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='menu_item',
                                 verbose_name=_('category'))
    image = models.ImageField(_("image"), upload_to='images/', blank=False)
    title = models.CharField(_("title"), max_length=30, unique=True, blank=False)
    slug = AutoSlugField(populate_from="title", unique=True, null=True)
    description = models.TextField(_("description"), max_length=200, blank=False)
    price = models.DecimalField(_("price"),
                                max_digits=5,
                                decimal_places=3,
                                validators=[MinValueValidator(0)],
                                default=0,
                                blank=True,
                                null=True,
                                )

    def __str__(self):
        return f'{self.title} : {self.price}'


# Employee
class MenuItemOption(models.Model):
    menu_item = models.ForeignKey(MenuItem, models.CASCADE, verbose_name=_('menu item option'),
                                  related_name='menu_item_option')
    field_name = models.CharField(_("field name"), max_length=30, blank=False, null=True)

    class Meta:
        unique_together = ['menu_item', 'field_name']

    def __str__(self):
        return f'{self.menu_item} : {self.field_name}'


# Employee
class OptionValue(models.Model):
    item_option = models.ForeignKey(MenuItemOption, on_delete=models.CASCADE, verbose_name=_('option value'),
                                    related_name='option_value', null=True, blank=True)
    value = models.CharField(verbose_name=_('value'), max_length=30, blank=True, null=True)
    price = models.DecimalField(_("price"), max_digits=5, decimal_places=3, validators=[MinValueValidator(0)],
                                blank=True, null=True,)

    class Meta:
        unique_together = ['item_option', 'value']

    def __str__(self):
        if self.value and self.price:
            return f"{self.value} : {self.price}"
        elif self.price is None:
            return f"{self.value}- {self.pk}"
