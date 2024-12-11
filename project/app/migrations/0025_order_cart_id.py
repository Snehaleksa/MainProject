# Generated by Django 5.1.2 on 2024-12-11 05:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_cart_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cart_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.cart'),
        ),
    ]
