# Generated by Django 5.0.2 on 2024-04-07 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_alter_cartitem_dish_option'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together=set(),
        ),
    ]
