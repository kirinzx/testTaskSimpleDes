# Generated by Django 4.2.6 on 2023-12-05 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buying', '0004_alter_order_discount_alter_order_tax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='buying.item'),
        ),
    ]
