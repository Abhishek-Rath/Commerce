from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("show_listing/<int:auction_id>", views.show_listing, name = "show_listing"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name = "add_to_watchlist"),
    path("remove_from_watchlist/<int:auction_id>", views.remove_from_watchlist, name = "remove_from_watchlist"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("bid_on_auction/<int:listing_id>", views.bid_on_auction, name = "bid_on_auction"),
    path("comment/<int:listing_id>", views.comment, name = "comment"),
    path("close_auction/<int:listing_id>", views.close_auction, name = "close_auction"),
    path("categories/<str:category>", views.categories, name="categories"),
]
