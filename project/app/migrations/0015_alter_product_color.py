# Generated by Django 5.1.2 on 2024-12-03 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_order_cart_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
