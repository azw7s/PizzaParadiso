from rest_framework import serializers
from .models import MenuItem, MenuCategory, MenuItemOption, OptionValue


class OptionValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionValue
        fields = ['pk', 'item_option', 'value', 'price']


class MenuItemOptionSerializer(serializers.ModelSerializer):
    option_value = OptionValueSerializer(many=True)

    class Meta:
        model = MenuItemOption
        fields = ['pk', 'menu_item', 'field_name', 'option_value']


class MenuItemSerializer(serializers.ModelSerializer):
    menu_item_option = MenuItemOptionSerializer(many=True)

    class Meta:
        model = MenuItem
        fields = ['pk', 'category', 'title', 'slug', 'description', 'price', 'image', 'menu_item_option']


class MenuCategorySerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(many=True)

    class Meta:
        model = MenuCategory
        fields = ['parent', 'name',  'menu_item']
