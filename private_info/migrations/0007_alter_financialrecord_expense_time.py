# Generated by Django 3.2.19 on 2023-06-19 19:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('private_info', '0006_memo_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialrecord',
            name='expense_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
