from django.contrib import admin
from .models import MenuItem, MenuCategory, MenuItemOption, OptionValue


class MenuCategoryAdmin(admin.ModelAdmin):
    model = MenuCategory


class MenuItemAdmin(admin.ModelAdmin):
    model = MenuItem


class OptionValueAdmin(admin.ModelAdmin):
    model = OptionValue


class ItemOptionAdmin(admin.ModelAdmin):
    model = MenuItemOption


admin.site.register(MenuItemOption, ItemOptionAdmin)
admin.site.register(MenuCategory, MenuCategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(OptionValue, OptionValueAdmin)
