# Generated by Django 5.0.7 on 2024-09-22 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Fruit', 'Fruit'), ('Vegetable', 'Vegetable'), ('Non-veg', 'Non-veg'), ('Breads', 'Breads'), ('All', 'All')], max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]
