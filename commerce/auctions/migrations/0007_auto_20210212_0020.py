# Generated by Django 3.1.5 on 2021-02-12 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210211_2320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionlisting',
            old_name='image',
            new_name='url',
        ),
        migrations.AlterField(
            model_name='bid',
            name='current_bid',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
