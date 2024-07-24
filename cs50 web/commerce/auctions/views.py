from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
import markdown2

md = markdown2.markdown

from .models import User, Listing, Watchlist, Bid, Comment
from .choices import CATEGORY_CHOICES


import markdown2

def index(request):
    listings = Listing.objects.all()

    for listing in listings:
        listing.description = md(listing.description)

    return render(request, "auctions/index.html", {
        'listings': listings
    })


def categories(request):
    if request.method == 'POST':
        category = request.POST.get('category').lower()
        listings = Listing.objects.filter(category=category)
        return render(request, 'auctions/category.html', {
            'listings': listings,
            'category': category
        })

    categories = [choice[1] for choice in CATEGORY_CHOICES]
    return render(request, "auctions/categories.html", {
        'categories': categories
    })

def listings(request, listing):
    if not Listing.objects.filter(id=listing).exists():
        message = f'Cannot find a listing with a id of {listing}.'
        return HttpResponseRedirect(reverse('not_found', args=[message]))

    listing_obj = Listing.objects.get(pk=listing)
    lister = listing_obj.lister
    watchlist, _ = Watchlist.objects.get_or_create(owner=request.user)
    is_in_watchlist = watchlist.listings.filter(id=listing).exists()

    has_a_bid = Bid.objects.filter(listing=listing).exists()

    message = request.GET.get('message', '')

    comments = Comment.objects.filter(listing=listing_obj)

    return render(request, 'auctions/listings.html', {
        'lister': lister,
        'listing': listing_obj,
        'is_in_watchlist': is_in_watchlist,
        'has_a_bid': has_a_bid,
        'message' : message,
        'comments': comments
    })

def close_listing(request, listing):
    listing_obj = Listing.objects.get(pk=listing)
    bids = Bid.objects.filter(listing=listing)
    winning_bid = bids.order_by('-bid').first()

    if request.user == listing_obj.lister:
        listing_obj.closed = True
        if winning_bid is not None:
            listing_obj.winner = winning_bid.bidder
        listing_obj.save()


    return HttpResponseRedirect(reverse('listings', args=[listing]))



@login_required
def bid(request, listing):
    if not Listing.objects.filter(id=listing).exists():
        message = f'Cannot find a listing with a id of {listing}.'
        return HttpResponseRedirect(reverse('not_found', args=[message]))

    listing_obj = Listing.objects.get(pk=listing)

    if not listing_obj.closed and listing_obj.lister != request.user:
        bid_value = request.POST.get('bid')

        if Bid.objects.filter(listing=listing).exists():
            bids = Bid.objects.filter(listing=listing)
            highest_bid = bids.order_by('-bid').first()
            if float(bid_value) and float(bid_value) >= highest_bid.bid + 1:
                new_bid = Bid.objects.create(
                    bidder=request.user,
                    listing=listing_obj,
                    bid=bid_value
                )
                listing_obj.current_price = new_bid.bid
                listing_obj.save()
                return HttpResponseRedirect(reverse('listings', args=[listing]))
            else:
                message = f'Your bid must be at least $1 higher than the current highest bid {highest_bid.bid}'
                return HttpResponseRedirect(reverse('listings', args=[listing]) + f'?message={message}')

        else:
            starting_bid = listing_obj.current_price
            if float(bid_value) and float(bid_value) >= starting_bid:
                new_bid = Bid.objects.create(
                    bidder=request.user,
                    listing=listing_obj,
                    bid=bid_value
                )
            else:
                message = f'Your bid must be higher or equal to {starting_bid}'
                return HttpResponseRedirect(reverse('listings', args=[listing]) + f'?message={message}')

        if new_bid is not None:
            listing_obj.current_price = new_bid.bid
            listing_obj.save()

    return HttpResponseRedirect(reverse('listings', args=[listing]))


@login_required
def watchlist(request, listing):
    if not Listing.objects.filter(id=listing).exists():
        message = f'Cannot find a listing with a id of {listing}.'
        return HttpResponseRedirect(reverse('not_found', args=[message]))

    listing_obj = Listing.objects.get(pk=listing)

    if not listing_obj.closed:
        watchlist, _ = Watchlist.objects.get_or_create(owner=request.user)


        if watchlist.listings.filter(id=listing).exists():
            watchlist.remove_listing(listing_obj)
            return HttpResponseRedirect(reverse('listings', args=[listing]))

        watchlist.add_listing(listing_obj)

    return HttpResponseRedirect(reverse('listings', args=[listing]))


def comment(request, listing):
    if not Listing.objects.filter(id=listing).exists():
        message = f'Cannot find a listing with a id of {listing}.'
        return HttpResponseRedirect(reverse('not_found', args=[message]))

    listing_obj = Listing.objects.get(pk=listing)

    comment = request.POST.get('comment')

    if not listing_obj.closed and comment:
        new_comment = Comment.objects.create(
            commenter = request.user,
            listing = listing_obj,
            comment = comment
        )

    return HttpResponseRedirect(reverse('listings', args=[listing]))



class ListingForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    current_price = forms.DecimalField(max_digits=8, decimal_places=2)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    picture = forms.ImageField(required=False)

@login_required
def create_listing(request):
    form = ListingForm()

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            current_price = form.cleaned_data['current_price']

            if current_price <= 0.00:
                return render(request, 'auctions/create_listing.html', {
                'form': form,
                'message': 'the starting price must be at least 0.01'
                })

            new_listing = Listing.objects.create(
                lister=request.user,
                **form.cleaned_data
            )

            return HttpResponseRedirect(reverse('listings', args=[new_listing.id]))

    return render(request, 'auctions/create_listing.html', {
        'form': form
    })

def view_watchlist(request):
    user = request.user
    watchlist = Watchlist.objects.filter(owner=user).first()
    return render(request, 'auctions/watchlist.html', {
        'watchlist': watchlist
    })


def login_view(request):
    if request.method == "POST":
        pass

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


def not_found(request, message):
    message = message

    return render(request, "auctions/not_found.html", {
        'message': message,
    }, status=404)