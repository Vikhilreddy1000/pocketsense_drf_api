# Generated by Django 5.1.4 on 2025-01-07 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0008_alter_expense_receipt_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='otp_sent_time',
        ),
        migrations.AddField(
            model_name='customuser',
            name='otp_verification',
            field=models.BooleanField(default=False),
        ),
    ]
