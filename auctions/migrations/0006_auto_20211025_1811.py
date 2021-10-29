# Generated by Django 3.2.7 on 2021-10-25 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_rename_item_bids_auctions_item_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctions',
            name='item_bid',
        ),
        migrations.AddField(
            model_name='auctions',
            name='bid',
            field=models.ManyToManyField(blank=True, related_name='bids', to='auctions.Bid'),
        ),
    ]