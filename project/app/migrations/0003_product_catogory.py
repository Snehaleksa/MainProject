# Generated by Django 5.1.2 on 2024-11-05 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='catogory',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
