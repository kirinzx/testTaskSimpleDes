# Generated by Django 4.2.6 on 2023-12-05 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buying', '0002_alter_discount_discount_percents_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tax',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
