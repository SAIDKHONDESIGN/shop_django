# Generated by Django 5.1.4 on 2025-01-07 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oson_app', '0012_rename_products_comment_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='in_stock',
            field=models.IntegerField(default=0, verbose_name='В наличии'),
        ),
    ]
