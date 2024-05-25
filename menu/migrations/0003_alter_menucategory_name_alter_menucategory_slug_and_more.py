# Generated by Django 4.2.8 on 2023-12-12 08:25

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_menucategory_delete_category_delete_ingredient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menucategory',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='menucategory',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_item', to='menu.menucategory', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='description',
            field=models.TextField(max_length=200, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(upload_to='menu/images/', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='title',
            field=models.CharField(max_length=50, unique=True, verbose_name='title'),
        ),
    ]
