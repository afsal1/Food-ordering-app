# Generated by Django 3.1.2 on 2020-11-21 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_ordering_app', '0011_vendor_offer_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='offer_id',
        ),
        migrations.AlterField(
            model_name='customer',
            name='status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
