# Generated by Django 4.2.8 on 2024-01-31 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_alter_itemoption_menu_item'),
        ('order', '0006_cartitem_dish_option'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'dish', 'dish_option')},
        ),
    ]
