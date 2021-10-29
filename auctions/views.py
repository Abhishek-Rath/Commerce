from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    auctions = Auctions.objects.all()
    return render(request, "auctions/index.html" ,{
        "auctions":auctions
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
def create(request):
    if request.method == "POST":
        user = User.objects.get(username = request.user)
        form = AuctionsForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            start_bid = form.cleaned_data['start_bid']
            category = form.cleaned_data['category']
            img = form.cleaned_data['image']
            auction_created = Auctions.objects.create(
                user = user,
                title = title,
                description = description,
                start_bid = start_bid,
                category = category,
                image = img
            )
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form":form
            })
        
    return render(request, "auctions/create.html", {
            "form":AuctionsForm()
    })


# @login_required(login_url = 'login')
# def show_listing(request, auction_id):
#     user = User.objects.get(username = request.user)       
#     listing = Auctions.objects.get(pk = auction_id)
#     form = BidForm()
#     message = ""
#     if form.is_valid():
#         price = float(form.cleaned_data["bid"])

#         print("User's bids", price)
#         if price >= listing.bid and price >= user.bids.all():
#             listing.bid = price
#         else:
#             message = "Bid should be greater than or equal to starting bid."
#     # else:
#     #     message = "The Auction for this item is closed!!"
@login_required(login_url = 'login')
def show_listing(request, auction_id):
    # form = BidForm(request.POST)
    # listing = Auctions.objects.get(pk = auction_id)
    # user = User.objects.get(username = request.user)
    # message = ""
    # if not listing.closed:
    #     if form.is_valid():
    #         price = form.cleaned_data["bid"]
    #         if(price >= listing.start_bid):
    #             form.user = user
    #             form.bid = price
    #             form.save()
    #             listing.item_bid.add(price)
    #             listing.start_bid = price
    #             listing.save()
    #             message = f"len({user.bids.all()}) bids placed so far. Your bid is the highest bid!!"

    # return render(request, "auctions/listing.html", {
    #     "listing":listing,
    #     "bid":form
    # })

    bid = BidForm()
    comment = CommentsForm()
    listing = Auctions.objects.get(pk = auction_id)

    if listing.closed:  
        return render(request, "auctions/listing.html", {
        "listing":listing,
        "bid":bid,
        "comment":comment,
        "message":"This listing is closed. You can't bid on this item.",
    })

    

    return render(request, "auctions/listing.html", {
        "listing":listing,
        "bid":bid,
        "comment":comment
    })

    # return render(request, "auctions/listing.html", {
    # "listing":listing,
    # "bid":BidForm(),
    # "message":message
    # })




@login_required
def add_to_watchlist(request, listing_id):
    user = User.objects.get(username = request.user)  # Get current user
    auction = Auctions.objects.get(pk = listing_id)
    item_present = user.watchlist.filter(auction = auction)
    if not item_present:
        watchlist = Watchlist()
        watchlist.user = user
        watchlist.auction = auction
        watchlist.save()
        return render(request, "auctions/watchlist.html", {
            "watchlist_items":user.watchlist.all(),   # particular user's watclist items,
            "message": f"Successfully added {auction.title} in your watchlist"
        }) 
    else :
         return render(request, "auctions/watchlist.html", {
            "watchlist_items":user.watchlist.all(),   
            "message":"Item already present in your list."
        }) 
        

def remove_from_watchlist(request, auction_id):
    user = User.objects.get(username = request.user)  # Get current user
    auction = Auctions.objects.get(pk = auction_id)
    item_present = user.watchlist.filter(auction = auction)
    if item_present:
        item_present.delete()
        return render(request, "auctions/watchlist.html", {
            "watchlist_items":user.watchlist.all(),   
            "message":"Successfully removed the item from your Watchlist."
        }) 

@login_required
def watchlist(request):
    user = User.objects.get(username = request.user)
    user_watchlist_items = user.watchlist.all()
    total_items_in_watchlist = len(user_watchlist_items)
    return render(request, "auctions/watchlist.html", {
        "watchlist_items":user_watchlist_items,
        "length":total_items_in_watchlist,
        "message":f"{total_items_in_watchlist} items present in your watchlist"
    })


def bid_on_auction(request, listing_id):
    listing = Auctions.objects.get(pk = listing_id)
    user = User.objects.get(username = request.user)
    price = int(request.POST["bid"])
    message = ""
    if not listing.closed:
        if user != listing.user :
            if(price >= listing.start_bid or price >= listing.last_bid):
                bid = Bid.objects.create(user = user, bid = price)
                listing.bid.add(bid)  # add user's bid to particular listing
                listing.last_bid = bid
                listing.save() # save current details of this listing
                message = f"{(listing.bid).count()} bid(s) so far. Your bid is the current bid."
                return render(request, "auctions/listing.html", {
                    "message":message,
                    "listing":listing,
                    "bid":BidForm(),
                    "comment":CommentsForm()
                })

            else:  # Handle bid <= start_bid
                message = "Your bid must be atleast higher than the initial bid!!"
                return render(request, "auctions/listing.html", {
                    "message":message,
                    "listing":listing,
                    "comment":CommentsForm()
                })

        else:   # Listing owner bids can;t bid on item
            message = "Listing Owner can't bid on listing😂😂"
            return render(request, "auctions/listing.html", {
                "message":message,
                "listing":listing,
                "bid":BidForm(),
                "comment":CommentsForm()
            })
        
    else: # listing is closed
        message = "This auction is closed, you can't bid on this item."
        return render(request, "auctions/listing.html", {
            "message":message,
            "listing":listing,
            "bid":BidForm(),
            "comment":CommentsForm(),
        })


def comment(request, listing_id):
    user = User.objects.get(username = request.user)
    listing = Auctions.objects.get(pk = listing_id)
    comment = request.POST["comment"]
    comments = Comments.objects.create(user = user, auction = listing, comment = comment)
    comments.save()
    return HttpResponseRedirect(reverse("show_listing", args=(listing.id,)))


def close_auction(request, listing_id):
    user = User.objects.get(username = request.user)
    listing = Auctions.objects.get(pk = listing_id)
    # if request.method == "GET":
    listing.closed = True
    listing.save()
        # message = "The auction for this item is closed!!"
    return HttpResponseRedirect(reverse("show_listing", args=(listing.id,)))
        # return redirect('index')

def categories(request, category):
    get_category = Category.objects.get(category = category)  # get category
    auctions = Auctions.objects.filter(category = get_category).order_by('id').reverse()  # get all listings of specific category
    user = User.objects.get(username = request.user)

    if user is not None:
        return render(request, "auctions/categories.html", {
            'auctions': auctions,
            'categories': get_category,
        })
    
    



