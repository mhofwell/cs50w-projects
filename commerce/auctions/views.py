from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.models import ModelForm
from django.forms.widgets import NumberInput
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import New_bid, User, CreateNewListing, AuctionListing, Bid, Comment


def index(request):
    if request.method == "POST":
        title = request.POST["title"]
        return HttpResponseRedirect(reverse("getpage", kwargs={'title': f"{title}"}))
    return render(request, "auctions/index.html", {
        'active_listings': AuctionListing.objects.all(),
        'users': User.objects.all(),
        'bid': Bid.objects.all(),
        'comment': Comment.objects.all()
    })


def getpage(request, title):
    listing = AuctionListing.objects.get(title=f"{title}")
    bid = Bid.objects.get(listing=listing)
    comments = Comment.objects.get(listing=listing)
    current_bid = bid.current_bid
    return render(request, "auctions/listingpage.html", {
        'listing': listing,
        'new_bid': New_bid(),
        'current_bid': current_bid,
        'comment_form': Comment(),
        'comments': comments
        # get all the comments for this bid.
        # send new comment ModelForm out to template.
    })


def bid(request):
    # determine where to add the validator for the bid > price and current_bid
    return render(request, "auctions/listingpage.html", {
    })


def comment(request):
    # determine where to add the validator for the bid > price and current_bid
    return render(request, "auctions/listingpage.html", {
    })


def new(request):
    user = User.objects.get(pk=request.user.id)
    print(user)
    if request.method == "POST":
        form = CreateNewListing(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.save()
            # clean up into a utility
            starting_bid = form.cleaned_data['price']
            title = form.cleaned_data['title']
            listing = AuctionListing.objects.get(title=title)
            new_bid = Bid(user=user, listing=listing,
                          current_bid=starting_bid)
            new_bid.save()
        return HttpResponseRedirect(reverse("index"))
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
