# Generated by Django 3.2.3 on 2024-07-14 19:03

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20240714_1403'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name': 'Подкатегория', 'verbose_name_plural': 'Подкатегории'},
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(upload_to='recipes/images/category', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(upload_to='recipes/images/category', verbose_name='Изображение'),
        ),
    ]