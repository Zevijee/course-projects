# Generated by Django 4.2.1 on 2023-05-22 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_starting_bid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='starting_bid',
            new_name='current_price',
        ),
    ]
