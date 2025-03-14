# Generated by Django 5.1.4 on 2025-01-07 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oson_app', '0007_slider'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Login',
        ),
        migrations.AlterField(
            model_name='products',
            name='full_description',
            field=models.TextField(verbose_name='Полное описание'),
        ),
        migrations.AlterField(
            model_name='products',
            name='short_description',
            field=models.TextField(max_length=40, verbose_name='Краткое описание'),
        ),
    ]
