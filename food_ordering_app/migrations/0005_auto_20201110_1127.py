# Generated by Django 3.1.2 on 2020-11-10 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_ordering_app', '0004_auto_20201109_1633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='image',
        ),
        migrations.AddField(
            model_name='vendor',
            name='vendor_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
