# Generated by Django 5.0.5 on 2024-11-30 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0008_rename_price_at_income_incomehistory_price_at_moment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderhistory',
            name='order_type',
            field=models.CharField(choices=[('sale', 'Продажа'), ('income', 'Поступление')], max_length=10, null=True),
        ),
    ]
