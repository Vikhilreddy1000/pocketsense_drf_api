# Generated by Django 5.1.4 on 2025-01-07 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0006_alter_settlement_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='receipt_image',
            field=models.ImageField(blank=True, null=True, upload_to='receipts/'),
        ),
    ]
