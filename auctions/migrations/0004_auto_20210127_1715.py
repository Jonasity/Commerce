# Generated by Django 3.1.3 on 2021-01-27 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210127_1654'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bid',
            new_name='Bids',
        ),
    ]
