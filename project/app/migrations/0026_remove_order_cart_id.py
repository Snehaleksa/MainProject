# Generated by Django 5.1.2 on 2024-12-11 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_order_cart_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart_id',
        ),
    ]
