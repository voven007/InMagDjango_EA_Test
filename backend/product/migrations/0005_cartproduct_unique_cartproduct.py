# Generated by Django 3.2.3 on 2024-07-16 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20240715_2149'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='cartproduct',
            constraint=models.UniqueConstraint(fields=('cart', 'product'), name='unique_cartproduct'),
        ),
    ]
