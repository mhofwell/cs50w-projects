from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.models import ModelForm
from django.forms.widgets import NumberInput
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Comment_form, New_bid, User, CreateNewListing, AuctionListing, Bid, Comment, Watchlist
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages


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
    print(listing.id)
    if Comment.objects.filter(listing=listing).exists():
        comments = Comment.objects.filter(listing=listing)
        return render(request, "auctions/listingpage.html", {
            'listing': listing,
            'new_bid': New_bid(),
            'comment_form': Comment_form(),
            'comments': comments
        })
    else:
        return render(request, "auctions/listingpage.html", {
            'listing': listing,
            'new_bid': New_bid(),
            'comment_form': Comment_form()
        })


def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    watchlist_object = Watchlist.objects.get(user=user)
    listings = watchlist_object.item.all()
    return render(request, "auctions/watchlist.html", {
        'watchlist': listings,
    })


@ login_required
def add_to_watchlist(request, listing_id):
    listing_to_save = get_object_or_404(AuctionListing, pk=listing_id)
    title = listing_to_save.title
    # Check if the item already exists in that user watchlist
    if Watchlist.objects.filter(user=request.user, item=listing_id).exists():
        messages.add_message(request, messages.ERROR,
                             "You already have it in your watchlist.")
        return HttpResponseRedirect(reverse("getpage", kwargs={'title': f"{title}"}))
    # Get the user watchlist or create it if it doesn't exists
    user_list, create = Watchlist.objects.get_or_create(user=request.user)
    # Add the item through the ManyToManyField (Watchlist => item)
    user_list.item.add(listing_to_save)
    messages.add_message(request, messages.SUCCESS,
                         "Successfully added to your watchlist")
    return HttpResponseRedirect(reverse("watchlist"))


@ login_required
def bid(request):
    if request.method == "POST":
        # get user details
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        # get listing details
        listing_title = request.POST["listing.title"]
        listing = AuctionListing.objects.get(title=listing_title)
        # get current bid object
        bid_obj = New_bid(request.POST)
        # check if bid object is valid
        if bid_obj.is_valid():
            # add required fields to bid object
            bid_obj.save(commit=False)
            bid_obj.user = user
            bid_obj.listing = listing
            bid_obj.save()
            # check to see if bid is the higest bid and save if so
            new_bid = request.POST["new_bid.bid"]
            starting_bid = listing.starting_bid
            highest_bid = listing.highest_bid
            if new_bid > starting_bid and new_bid > highest_bid:
                listing.highest_bid = new_bid

    pass


@ login_required
def comment(request):
    return render(request, "auctions/listingpage.html", {
    })


@ login_required
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
            # starting_bid = form.cleaned_data['price']
            # title = form.cleaned_data['title']
            # listing = AuctionListing.objects.get(title=title)
            # new_bid = Bid(user=user, listing=listing,
            #               current_bid=starting_bid)
            # new_bid.save()
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
