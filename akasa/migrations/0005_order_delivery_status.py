# Generated by Django 5.0.7 on 2024-09-22 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akasa', '0004_item_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(default='Pending', max_length=50),
        ),
    ]
