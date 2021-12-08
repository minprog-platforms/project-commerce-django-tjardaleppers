from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from django.utils import timezone

class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    starting_price = models.CharField(max_length=7)
    current_price = models.CharField(max_length=7)
    image = models.URLField()
    category = models.CharField(max_length=65)
    seller = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    listing_time = models.DateTimeField(default=timezone.now)
    closed = models.BooleanField(default=False)

class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    listing = models.ForeignKey(AuctionListings, on_delete=CASCADE)
    bid_price = models.CharField(max_length=7)
    bid_time = models.DateTimeField()
    
class Comments(models.Model):
    listing = models.ForeignKey(AuctionListings, on_delete=CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    comment_body = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
