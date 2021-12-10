from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import AuctionListings, Comments, Bids

class CreateListing(forms.ModelForm):
    title = forms.CharField(required=True, label="Title", label_suffix="", widget=forms.TextInput(attrs={'placeholder':'Title'}))
    description = forms.CharField(required=True, label="Description", label_suffix="", widget=forms.Textarea(attrs={'placeholder':'Description', 'cols': '100px'}))
    starting_price = forms.DecimalField(required=True, label="Starting price", label_suffix="", widget=forms.NumberInput(attrs={'placeholder':'Starting price'}))
    image = forms.URLField(required=True, label="Image URL", label_suffix="", widget=forms.URLInput(attrs={'placeholder':'Image URL'}))
    category = forms.CharField(required=True, label="Category", label_suffix="", widget=forms.TextInput(attrs={'placeholder':'Category'}))
    class Meta:
        model = AuctionListings
        fields = ["title", "description", "starting_price", "image", "category"]

class AddComment(forms.ModelForm):
    comment = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder':'Comment'}))
    class Meta:
        model = Comments
        fields = ["comment"]

class AddBid(forms.ModelForm):
    bid_price = forms.DecimalField(required=True, widget=forms.NumberInput(attrs={'placeholder':'Bid price'}))
    class Meta:
        model = Bids
        fields = ["bid_price"]
