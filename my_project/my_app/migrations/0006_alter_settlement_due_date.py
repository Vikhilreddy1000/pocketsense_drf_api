# Generated by Django 5.1.4 on 2025-01-07 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0005_remove_expense_split_with_expense_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settlement',
            name='due_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
