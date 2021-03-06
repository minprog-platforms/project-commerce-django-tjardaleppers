from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    # path("login"), auth_views.LoginView.as_view(),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/new-comment/<int:listing_id>", views.add_comment, name="new comment"),
    path("listing/new-bid/<int:listing_id>", views.add_bid, name="new bid"),
    path("listing/close-listing/<int:listing_id>", views.closelisting, name="close listing")
]
