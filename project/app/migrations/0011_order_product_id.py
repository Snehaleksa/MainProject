# Generated by Django 5.1.2 on 2024-11-27 09:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_product_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.product'),
        ),
    ]
