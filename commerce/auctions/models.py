from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, date


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    listing_title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    category = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    current_bid = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/')
    date_created = models.DateField(auto_now_add=True)


class Bid(models.Model):
    pass


class Comment(models.Model):
    pass

# Auction listings

# Bids

# Comments on auction listings
