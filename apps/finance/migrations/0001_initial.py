# Generated by Django 5.0.5 on 2024-12-29 10:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='expenses', verbose_name='Изображение')),
                ('expend_type', models.CharField(choices=[('rent', 'Аренда'), ('utilities', 'Коммунальные услуги'), ('salaries', 'Зарплаты'), ('supplies', 'Поставки'), ('other', 'Другое')], max_length=50, verbose_name='Тип расхода')),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.shop', verbose_name='Магазин')),
            ],
        ),
    ]
