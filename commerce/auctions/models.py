from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, date


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    listing_title = models.CharField(max_length=100, default="None")
    description = models.TextField(max_length=500, default="None")
    category = models.CharField(max_length=25, default="None")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    current_bid = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='auctions/uploads/')
    date_created = models.DateField(auto_now_add=True)


class Bid(models.Model):
    pass


class Comment(models.Model):
    pass

# Auction listings

# Bids

# Comments on auction listings
