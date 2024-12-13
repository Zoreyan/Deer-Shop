# Generated by Django 5.0.5 on 2024-12-13 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='about',
            field=models.TextField(blank=True, null=True, verbose_name='О нас'),
        ),
        migrations.AddField(
            model_name='shop',
            name='contacts',
            field=models.TextField(blank=True, null=True, verbose_name='Контакты'),
        ),
        migrations.AddField(
            model_name='shop',
            name='coordinates',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Координаты'),
        ),
        migrations.AddField(
            model_name='shop',
            name='opening_hours',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Часы работы'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='image',
            field=models.ImageField(blank=True, default='shops/default_products.png', null=True, upload_to='shops', verbose_name='Изображение'),
        ),
    ]
