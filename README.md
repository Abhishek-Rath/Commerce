# Auction Site


### This project is part of [CS50 Web Development with Python and JavaScript](https://cs50.harvard.edu/web/2020/).

#### Link to project description is - https://cs50.harvard.edu/web/2020/projects/2/commerce/

The project is an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”


# Specifications
The project has following specifications:-
1. **Models**: The auction site contains the following models:
    - **Auctions:** Contains details about the particular auction - user, title, description, starting bid, category, image
    - **Bids:** Details about the user's bid on listings.
    - **Watchlist:** User's watchlist items.
    - **Comments:** Comments on a particular listing


2. **Create Listing:** Users can visit a page to create a new listing. They must specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image.

3. **Active Listings Page:** The default route of this web application lets the users view all of the currently active auction listings. 

4. **Listing Page:** Clicking on a particular listing takes users to a page specific to that listing. On that page, users should be able to view all details about the listing, including the current price for the listing.
    - Signed in users can add items to their watchlist. If item is already present the user can remove it.
    - Signed in users can bid on the item. Bid must be larger than the specified amount.
    - Signed in users can add comment to listig items.
    - If the useris signed in and is the one who created the listing, the user has the ability to “close” the auction from this page, which makes the highest bidder the winner   
      of the auction and makes the listing no longer active.
    - If a user is signed in on a closed listing page, and the user has won that auction, the page should say so. 

5. **Watchlist:** Users who are signed in are able to visit a Watchlist page, which displays all of the listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.

6. **Django Admin Interface:** Via the Django admin interface, a site administrator is able to view, add, edit, and delete any listings, comments, and bids made on the site.



## Link to YouTube Video:- https://youtu.be/Emtos6xCjs4


## Features to be added in future:
1. Delete specific auction.
2. Mobile Responsive.
3. Add more CSS



