# Generated by Django 5.1.4 on 2025-01-02 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oson_app', '0006_comment_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preview', models.ImageField(upload_to='images/slider', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Слайдер',
                'verbose_name_plural': 'Слайдеры',
            },
        ),
    ]
