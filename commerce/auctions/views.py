from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.models import ModelForm
from django.forms.widgets import NumberInput
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Comment_form, New_bid, User, CreateNewListing, AuctionListing, Bid, Comment, Watchlist, Categories
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages


def index(request):
    if request.method == "POST":
        pk = request.POST["pk"]
        return HttpResponseRedirect(reverse("getpage", kwargs={'pk': pk}))
    return render(request, "auctions/index.html", {
        'active_listings': AuctionListing.objects.all(),
        'users': User.objects.all(),
        'bid': Bid.objects.all(),
        'comment': Comment.objects.all(),
    })


def filter(request, name):
    print(name)
    if AuctionListing.objects.filter(category=name).exists():
        filtered_listings = AuctionListing.objects.filter(category=name)
        print(type(filtered_listings))
        return render(request, "auctions/categorypage.html", {
            'listings': filtered_listings,
            'category': name,
        })
    else:
        messages.add_message(request, messages.ERROR,
                             "No active items in that category!")
        return HttpResponseRedirect(reverse("categories"))


def categories(request):
    return render(request, "auctions/categories.html", {
        'categories': Categories
    })


def getpage(request, pk):
    user = request.user.id
    listing = AuctionListing.objects.get(pk=pk)
    creator = listing.user.id
    if listing.highest_bid_user:
        highest_bid = listing.highest_bid_user
        if Comment.objects.filter(listing=listing).exists():
            comments = Comment.objects.filter(listing=listing)
            return render(request, "auctions/listingpage.html", {
                'listing': listing,
                'new_bid': New_bid(),
                'comment_form': Comment_form(),
                'comments': comments,
                'creator': creator,
                'current_user': user,
                'highest_bid_user_id': highest_bid.pk
            })
        else:
            return render(request, "auctions/listingpage.html", {
                'listing': listing,
                'new_bid': New_bid(),
                'comment_form': Comment_form(),
                'current_user': user,
                'creator': creator,
                'highest_bid_user_id': highest_bid.pk
            })
    else:
        if Comment.objects.filter(listing=listing).exists():
            comments = Comment.objects.filter(listing=listing)
            return render(request, "auctions/listingpage.html", {
                'listing': listing,
                'new_bid': New_bid(),
                'comment_form': Comment_form(),
                'comments': comments,
                'creator': creator,
                'current_user': user,
            })
        else:
            return render(request, "auctions/listingpage.html", {
                'listing': listing,
                'new_bid': New_bid(),
                'comment_form': Comment_form(),
                'current_user': user,
                'creator': creator,
            })


@ login_required
def close(request, title):
    user = request.user
    listing = AuctionListing.objects.get(title=title, user=user)
    listing.active = False
    listing.save()

    return HttpResponseRedirect(reverse("index"))


@ login_required
def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    if Watchlist.objects.filter(user=user).exists():
        watchlist_object = Watchlist.objects.get(user=user)
        listings = watchlist_object.item.all()
        return render(request, "auctions/watchlist.html", {
            'watchlist': listings,
            'user': user
        })
    else:
        messages.add_message(request, messages.ERROR,
                             "You need to add an item to your watchlist first!")
        return HttpResponseRedirect(reverse("index"))


@ login_required
def add_to_watchlist(request, listing_id):
    listing_to_save = get_object_or_404(AuctionListing, pk=listing_id)
    title = listing_to_save.title
    # Check if the item already exists in that user watchlist
    if Watchlist.objects.filter(user=request.user, item=listing_id).exists():
        messages.add_message(request, messages.ERROR,
                             "You already have it in your watchlist.")
        return HttpResponseRedirect(reverse("getpage", kwargs={'pk': listing_id}))
    # Get the user watchlist or create it if it doesn't exists
    user_list, create = Watchlist.objects.get_or_create(user=request.user)
    # Add the item through the ManyToManyField (Watchlist => item)
    user_list.item.add(listing_to_save)
    messages.add_message(request, messages.SUCCESS,
                         "Successfully added to your watchlist")
    return HttpResponseRedirect(reverse("watchlist"))


@ login_required
def bid(request, pk):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        listing = AuctionListing.objects.get(pk=pk)
        bid = New_bid(request.POST)
        if bid.is_valid():
            bid_obj = bid.save(commit=False)
            bid_obj.user = user
            bid_obj.listing = listing
            bid_obj.save()
            # check to see if bid is the higest bid and save if so
            new_bid = bid_obj.bid
            starting_bid = listing.starting_bid
            highest_bid = listing.highest_bid
            if new_bid > starting_bid and new_bid > highest_bid:
                listing.highest_bid = new_bid
                listing.highest_bid_user = user
                listing.save()
                listing_id = listing.id
                add_to_watchlist(request, listing_id)
                messages.add_message(request, messages.SUCCESS,
                                     "Bid added!")
                return HttpResponseRedirect(reverse("getpage", kwargs={'pk': pk}))
            else:
                messages.add_message(request, messages.ERROR,
                                     "You need to match or exceed the current price or highest bid.")
                return HttpResponseRedirect(reverse("getpage", kwargs={'pk': pk}))
        else:
            messages.add_message(request, messages.ERROR,
                                 "You need to match or exceed the current price or highest bid.")
            return HttpResponseRedirect(reverse("getpage", kwargs={'pk': pk}))


@ login_required
def comment(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == "POST":
        obj = Comment_form(request.POST)
        pk = request.POST['pk']
        print(title)
        if obj.is_valid:
            comment_obj = obj.save(commit=False)
            print(comment_obj.user_comment)
            listing = AuctionListing.objects.get(pk=pk)
            comment_obj.listing = listing
            comment_obj.user = user
            comment_obj.save()
        return HttpResponseRedirect(reverse("getpage", kwargs={'pk': pk}))


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
