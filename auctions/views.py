from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import AuctionListings, User
from .forms import CreateListing


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
            new_listing.save()

            return render(request, "auctions/listing.html", {
                "listing": new_listing
            })
        else:
            raise Exception        
    else:
        form = CreateListing()

        return render(request, "auctions/create-listing.html", {
            "form": form
        })

@login_required
def listing(request, listing_id):
    listing = AuctionListings.objects.get(pk=listing_id)
    print(f"The listing id is: {listing_id}")

    return render(request, "auctions/listing.html", {
        "listing": listing
    })

# @login_required
# def comment(request, listing_id):
#     user = request.user
#     listing = AuctionListings.objects.get(pk=listing_id)
