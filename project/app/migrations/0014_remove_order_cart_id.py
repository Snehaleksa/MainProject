# Generated by Django 5.1.2 on 2024-12-03 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_product_color_product_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart_id',
        ),
    ]
