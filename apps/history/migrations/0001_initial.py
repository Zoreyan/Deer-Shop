# Generated by Django 5.1.2 on 2024-11-17 04:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomeHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price_at_income', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.shop')),
            ],
            options={
                'verbose_name': 'История поставки',
                'verbose_name_plural': 'История поставки',
            },
        ),
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('change', models.FloatField()),
                ('discount', models.FloatField(null=True)),
                ('profit', models.FloatField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.shop')),
            ],
            options={
                'verbose_name': 'История заказа',
                'verbose_name_plural': 'История заказа',
            },
        ),
        migrations.CreateModel(
            name='SoldHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price_at_sale', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='history.orderhistory')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.shop')),
            ],
            options={
                'verbose_name': 'История продаж',
                'verbose_name_plural': 'История продаж',
            },
        ),
    ]
