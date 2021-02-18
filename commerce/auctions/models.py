from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, date, timezone
from django.db.models.deletion import CASCADE, RESTRICT
from django.forms import ModelForm
from django import forms
from django.forms.models import BaseInlineFormSet
from django.forms.widgets import NumberInput, TextInput, Textarea
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator
from django.contrib.auth.decorators import login_required

CATEGORIES = [
    ('apparel', 'Apparel'),
    ('footwear', 'Footwear'),
    ('home', 'Home'),
    ('accessories', 'Accessories'),
    ('sporting goods', 'Sporting Goods')
]


# Models


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    user = models.ForeignKey(
        User, related_name='listings', on_delete=CASCADE)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    category = models.CharField(max_length=25, blank=True, choices=CATEGORIES)
    price = models.DecimalField(
        blank=True, max_digits=15, decimal_places=2, validators=[MinValueValidator(1)])
    img_url = models.URLField()
    date_created = models.DateTimeField(
        auto_now_add=True)
    active = models.BooleanField(max_length=5, default="True")

    def __str__(self):
        return f"{self.user}: {self.title}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(AuctionListing, related_name="watchlist")

    def __str__(self):
        return f"{self.user}'s watch list."


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments', default="None")
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name='comments', default="None")
    comment = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return (f"{self.comment} by {self.user}")


class Bid(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bids', default="None")
    listing = models.ForeignKey(
        AuctionListing, models.CASCADE, related_name='bids', default="None")
    current_bid = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(1)])
    bid_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        bid_time = self.bid_time
        formatted_time = bid_time.strftime('%Y-%m-%d %H:%M:%S')
        return f"Current bid is {self.current_bid} placed on {formatted_time} by {self.user}."


# ModelForms
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


class Comment_form(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        lables = {
            'comment': 'comment',
        }

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Great looking item...', 'cols': 10, 'rows': 3}),
        }


class New_bid(ModelForm):
    class Meta:
        model = Bid
        fields = ['current_bid']

        lables = {
            'current_bid': 'current_bid',
        }

        widgets = {
            'current_bid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '$0.00'})
        }

    # def clean(self):
    #     project = self.listing

    #     super(User_bid, self).clean()

    #     current_bid = self.cleaned_data.get('current_bid')
    #     = self.cleaned_data.get('password')

    #     # validating the username and password
    #     if len(username) < 5:
    #         self._errors['username'] = self.error_class(
    #             ['A minimum of 5 characters is required'])

    #     if len(password) < 8:
    #         self._errors['password'] = self.error_class(
    #             ['Password length should not be less than 8 characters'])

    #     return self.cleaned_data
