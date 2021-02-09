from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.widgets import NumberInput
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, AuctionListing

CATEGORIES = [
    ('apparel', 'Apparel'),
    ('footwear', 'Footwear'),
    ('home', 'Home'),
    ('accessories', 'Accessories'),
    ('sporting goods', 'Sporting Goods')
]


class CreateNewListing(forms.Form):
    listing_title = forms.CharField(required="true", label="listing_title", max_length=100,  widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your listing title.'}))
    description = forms.CharField(required="true", label="description", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Enter a descripton of your listing.', 'cols': 45, 'rows': 10}))
    category = forms.CharField(required="true",
                               label="Product Category", max_length=25, widget=forms.Select(choices=CATEGORIES))
    image = forms.ImageField(required="true", label="image")
    price = forms.DecimalField(required="true",
                               label="price", max_digits=10, decimal_places=2, min_value=0, widget=forms.NumberInput(attrs={'placeholder': '$0.00'}))


def index(request):
    return render(request, "auctions/index.html")


def new(request):
    if request.method == "POST":
        form = CreateNewListing(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["listing_title"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]
            print(f"{title}, {description}, {category}, {price}")

    return render(request, "auctions/new.html", {
        'form': CreateNewListing()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
