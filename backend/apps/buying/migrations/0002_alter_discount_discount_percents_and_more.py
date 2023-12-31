# Generated by Django 4.2.6 on 2023-12-05 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buying', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='discount_percents',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name='tax',
            name='tax_percents',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
    ]
