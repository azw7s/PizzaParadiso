# Generated by Django 5.0.2 on 2024-04-07 03:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0020_alter_cartitem_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(20)], verbose_name='quantity'),
        ),
    ]
