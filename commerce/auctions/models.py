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
    listing_title = models.CharField(max_length=100)
    description = models.TextField(
        max_length=500)
    category = models.CharField(max_length=25)
    starting_bid = models.FloatField(default=0.00)
    current_bid = models.FloatField(default=0.00)
    image = models.ImageField(upload_to='auctions/uploads/')
    date_created = models.DateField(auto_now_add=True)


class Bid(models.Model):
    pass


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
    starting_bid = forms.DecimalField(
        max_digits=10, decimal_places=2, min_value=0, initial=0.000)

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
            'description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter a descripton of your listing.', 'cols': 45, 'rows': 10}),
            'category': forms.Select(choices=CATEGORIES),
        }
