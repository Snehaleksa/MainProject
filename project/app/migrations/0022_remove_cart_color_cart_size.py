# Generated by Django 5.1.2 on 2024-12-05 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_product_color_remove_product_size_product_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='color',
        ),
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
