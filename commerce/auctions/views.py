from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.models import ModelForm
from django.forms.widgets import NumberInput
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .utils import download_img
from .models import User, CreateNewListing, AuctionListing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        'active_listings': AuctionListing.objects.all(),
        'users': User.objects.all(),
        'bid': Bid.objects.all(),
        'comment': Comment.objects.all()
    })


def new(request):
    if request.method == "POST":
        form = CreateNewListing(request.POST, request.FILES)
        if form.is_valid():
            url = form.cleaned_data["img_url"]
            path = download_img(request, url, form)
            print(path)
            form.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/new.html", {
        'form': CreateNewListing(),
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
