# Generated by Django 3.1.3 on 2021-01-27 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20210127_1715'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bids',
            new_name='Bid',
        ),
    ]
