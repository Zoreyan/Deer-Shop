# Generated by Django 5.1.2 on 2024-11-22 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_expense_delete_expend'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='date',
            new_name='created',
        ),
    ]
