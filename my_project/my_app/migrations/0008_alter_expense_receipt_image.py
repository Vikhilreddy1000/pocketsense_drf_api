# Generated by Django 5.1.4 on 2025-01-07 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0007_expense_receipt_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='receipt_image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
