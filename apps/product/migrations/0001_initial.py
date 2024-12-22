# Generated by Django 5.0.5 on 2024-12-21 10:44

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='shops/default_products.png', null=True, upload_to='shops', verbose_name='Изображение')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('coordinates', models.CharField(blank=True, max_length=100, null=True, verbose_name='Координаты')),
                ('contacts', models.TextField(blank=True, null=True, verbose_name='Контакты')),
                ('about', models.TextField(blank=True, null=True, verbose_name='О нас')),
                ('opening_hours', models.CharField(blank=True, max_length=255, null=True, verbose_name='Часы работы')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.category', verbose_name='Родительская категория')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.shop', verbose_name='Магазин')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Продажная цена')),
                ('unit', models.CharField(choices=[('шт', 'шт'), ('кг', 'кг')], default='шт', max_length=2, null=True, verbose_name='Единица измерения')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products', verbose_name='Изображение')),
                ('bar_code', models.CharField(max_length=100, null=True, unique=True, verbose_name='Штрихкод')),
                ('quantity', models.IntegerField(default=0, verbose_name='Количество')),
                ('min_quantity', models.IntegerField(default=0, verbose_name='Минимальный остаток')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category', verbose_name='Категория')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.shop', verbose_name='Магазин')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
    ]
