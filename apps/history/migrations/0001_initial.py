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
            name='OrderHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('change', models.FloatField(blank=True, null=True)),
                ('discount', models.FloatField(blank=True, null=True)),
                ('profit', models.FloatField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order_type', models.CharField(choices=[('sale', 'Продажа'), ('income', 'Поступление')], max_length=10, null=True)),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.shop')),
            ],
            options={
                'verbose_name': 'История заказа',
                'verbose_name_plural': 'История заказа',
            },
        ),
        migrations.CreateModel(
            name='IncomeHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price_at_moment', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.shop')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='history.orderhistory')),
            ],
            options={
                'verbose_name': 'История поставки',
                'verbose_name_plural': 'История поставки',
            },
        ),
        migrations.CreateModel(
            name='SoldHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_at_moment', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
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
