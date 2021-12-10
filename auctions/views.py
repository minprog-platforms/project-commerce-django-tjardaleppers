from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import AuctionListings, User
from .forms import CreateListing, AddComment, AddBid


def index(request):
    listings = AuctionListings.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listings
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

@login_required
def create_listing(request):
    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.seller = request.user
            new_listing.current_price = new_listing.starting_price
            new_listing.save()

            return render(request, "auctions/listing.html", {
                "listing": new_listing
            })
        else:
            raise Exception("Form is invalid")       
    else:
        form = CreateListing()

        return render(request, "auctions/create-listing.html", {
            "form": form
        })

@login_required
def listing(request, listing_id):
    listing = AuctionListings.objects.get(pk=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing
    })

@login_required
def add_comment(request, listing_id):
    listing = AuctionListings.objects.get(pk=listing_id)

    if request.method == "POST":
        form = AddComment(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.listing = listing
            new_comment.comment_body = form.cleaned_data["comment"]
            new_comment.save()

            # return to listing view
            return redirect('listing', listing_id)

        else:
            raise Exception("Form is invalid")
    else:
        form = AddComment()

        return render(request, "auctions/new_comment.html", {
            "form": form,
            "listing": listing
        })

@login_required
def add_bid(request, listing_id):
    listing = AuctionListings.objects.get(pk=listing_id)

    if request.method == "POST":
        form = AddBid(request.POST)
        if form.is_valid():
            new_bid = form.save(commit=False)
            new_bid.bidder = request.user
            new_bid.listing = listing
            new_bid.bid_price = form.cleaned_data["bid_price"]
            

            if new_bid.bid_price <= listing.current_price:
                return render(request, "auctions/new_bid.html", {
                    "listing": listing,
                    "form": form,
                    "message": "The bidding amount should be higher than the last bid or starting price."
                })
            else:
                new_bid.save()
                listing.current_price = new_bid.bid_price
                listing.save()
                print(f"bid price: {new_bid.bid_price}, current: {listing.current_price}")

                # return to listing view
                return redirect('listing', listing_id)
        
        else:
            raise Exception("Form is invalid")
    else:
        form = AddBid()

        return render(request, "auctions/new_bid.html", {
            "form": form,
            "listing": listing
        })

def closelisting(request, listing_id):
    listing = AuctionListings.objects.get(pk=listing_id)

    if request.method == "POST":
        listing.closed = True
        listing.save()
    else: 
        raise Exception("Not allowed")
    
    # return to listing view
    return redirect('listing', listing_id)
