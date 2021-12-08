from django.contrib import admin
from .models import User, AuctionListings, Comments, Bids

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListings)
admin.site.register(Comments)
admin.site.register(Bids)
