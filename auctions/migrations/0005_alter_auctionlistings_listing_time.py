# Generated by Django 3.2.9 on 2021-12-07 11:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20211207_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='listing_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
