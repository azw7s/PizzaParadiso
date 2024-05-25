# Generated by Django 4.2.8 on 2024-01-18 07:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_menuitem_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], max_length=10, verbose_name='size')),
                ('crust', models.CharField(choices=[('pan', 'Pan'), ('san francisco', 'San Francisco'), ('thin', 'Thin')], max_length=20, verbose_name='crust')),
                ('price', models.DecimalField(decimal_places=3, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('mneu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.menuitem')),
            ],
        ),
    ]
