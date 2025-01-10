# Generated by Django 5.1.4 on 2025-01-07 12:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oson_app', '0009_products_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductsGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/products', verbose_name='Изображение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oson_app.products', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Галерея товара',
                'verbose_name_plural': 'Галерея товаров',
            },
        ),
    ]
