# Generated by Django 3.1.2 on 2020-12-03 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_ordering_app', '0014_orderdetails_product_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='expiry_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]