# Generated by Django 5.1.2 on 2024-12-05 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_remove_order_cart_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
    ]
