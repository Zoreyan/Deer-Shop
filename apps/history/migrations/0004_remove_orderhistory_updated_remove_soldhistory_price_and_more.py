# Generated by Django 5.1.2 on 2024-11-22 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0003_alter_soldhistory_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderhistory',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='soldhistory',
            name='price',
        ),
        migrations.RemoveField(
            model_name='soldhistory',
            name='updated',
        ),
    ]
