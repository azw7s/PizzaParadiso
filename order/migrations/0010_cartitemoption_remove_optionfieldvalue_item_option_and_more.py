# Generated by Django 4.2.8 on 2024-02-06 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0015_menuitemoption_optionvalue_delete_optionfieldname'),
        ('order', '0009_itemoption_alter_cartitem_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItemOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='order.cartitem', verbose_name='cart item')),
                ('option_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option_value', to='menu.optionvalue', verbose_name='option value')),
            ],
        ),
        migrations.RemoveField(
            model_name='optionfieldvalue',
            name='item_option',
        ),
        migrations.DeleteModel(
            name='ItemOption',
        ),
        migrations.DeleteModel(
            name='OptionFieldValue',
        ),
    ]
