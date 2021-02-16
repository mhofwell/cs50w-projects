from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, date, timezone
from django.db.models.deletion import CASCADE, RESTRICT
from django.forms import ModelForm
from django import forms
from django.forms.models import BaseInlineFormSet
from django.forms.widgets import NumberInput, TextInput, Textarea


# Models

class AuctionListing(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    category = models.CharField(max_length=25, blank=True)
    price = models.DecimalField(
        blank=True, max_digits=15, decimal_places=2)
    img_url = models.URLField()
    date_created = models.DateTimeField(
        auto_now_add=True)
    Active = models.BooleanField(max_length=5, default="True")

    def __str__(self):
        return f"{self.title}"


class User(AbstractUser):
    listings = models.ForeignKey(
        AuctionListing, models.SET_NULL, related_name="owner", null=True)
    watchlist = models.ForeignKey(
        AuctionListing, models.SET_NULL, related_name="watchlist", null=True)
    won = models.ForeignKey(
        AuctionListing, models.SET_NULL, related_name="won", null=True)


class Comment(models.Model):
    pass
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commentor', default="None")
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name='listing', default="None")
    comment = models.TextField(max_length=500, blank=True, default="None")


class Bid(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bidder', default="None")
    listing = models.ForeignKey(
        AuctionListing, models.CASCADE, related_name='product', default="None")
    current_bid = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    bid_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        bid_time = self.bid_time
        formatted_time = bid_time.strftime('%Y-%m-%d %H:%M:%S')
        return f"{self.listing} current bid is {self.current_bid} placed on {formatted_time} by {self.user}."


# ModelForms

CATEGORIES = [
    ('apparel', 'Apparel'),
    ('footwear', 'Footwear'),
    ('home', 'Home'),
    ('accessories', 'Accessories'),
    ('sporting goods', 'Sporting Goods')


]


class CreateNewListing(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'category',
                  'price', 'img_url']
        labels = {
            'title': 'title',
            'description': 'description',
            'category': 'category',
            'price': 'price',
            'img_url': 'img_url',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your listing title.'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter a descripton of your listing.', 'cols': 45, 'rows': 10}),
            'category': forms.Select(attrs={'class': 'form-control'}, choices=CATEGORIES),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '$0.00'}),
            'img_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'www.example.com/yourimage.jpg'})
        }


class Comments(ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'listing', 'comment']

        lables = {
            'user': 'user',
            'listing': 'listing',
            'comment': 'comment',
        }

    widgets = {

    }
