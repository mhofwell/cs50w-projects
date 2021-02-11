from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, date
from django.forms import ModelForm
from django import forms
from django.forms.models import BaseInlineFormSet
from django.forms.widgets import NumberInput, TextInput, Textarea


# Models

class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    listing_title = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    category = models.CharField(max_length=25, blank=True)
    starting_bid = models.DecimalField(
        blank=True, max_digits=15, decimal_places=2, default=0.00)
    # current_bid = models.ForeignKey(
    #     Bid, on_delete=models.CASCADE, related_name="current_bid")
    image = models.URLField()
    date_created = models.DateTimeField(auto_now_add=True)


class Bid(models.Model):
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="listing", blank=True)
    current_bid = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    bid_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bid_by", null=True)
    bid_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.listing} current bid is {self.current_bid} placed on {self.bid_time} by {self.bid_by}."


class Comment(models.Model):
    pass


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
        fields = ['listing_title', 'description', 'category',
                  'starting_bid', 'image']
        labels = {
            'listing_title': 'title',
            'description': 'description',
            'category': 'category',
            'starting_bid': 'starting_bid',
            'image': 'image'
        }
        widgets = {
            'listing_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your listing title.'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter a descripton of your listing.', 'cols': 45, 'rows': 10}),
            'category': forms.Select(attrs={'class': 'form-control'}, choices=CATEGORIES),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.TextInput(attrs={'class': 'form-control'})
        }
