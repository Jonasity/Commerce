from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import models
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    return HttpResponseRedirect(reverse("activelisting"))


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


@login_required(login_url='/login')
def activelisting(request):
    products = Listing.objects.all()
    empty = False
    if len(products) == 0:
        empty = True
    return render(request, "auctions/activelisting.html", {
        "products": products,
        "empty": empty
    })


@login_required(login_url='/login')
def viewlisting(request, product_id):
    if request.method == "POST":
        item = Listing.objects.get(id=product_id)
        newbid = int(request.POST.get('newbid'))

        if item.starting_bid >= newbid:

            return render(request, "auctions/viewlisting.html", {
                "product": item, 
                "message": "Your bid is too low"
            })
        else: 
            item.starting_bid = newbid
            item.save()
            #input info to BID model
            objBid = Bid()
            objBid.user = request.user.username
            objBid.bid_amount = newbid
            objBid.title = item.title
            objBid.listingid = product_id
            objBid.save()
            return render(request, "auctions/viewlisting.html", {
                "product": item
            })
    else:
        product = Listing.objects.get(id=product_id)
        watchlist = Watchlist.objects.filter(listingid = product_id, user = request.user.username)
        comments = Comments.objects.filter(listingid = product_id)
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "watch": watchlist,
            "comments": comments
        })

@login_required(login_url='/login')
def createlisting(request):
    if request.method == "POST":
        objListing = Listing()
        objListing.seller = request.user.username   
        objListing.title = request.POST.get('title')
        objListing.description = request.POST.get('description')
        objListing.starting_bid = request.POST.get('starting_bid')
        objListing.image_link = request.POST.get('image_link')
        objListing.category = request.POST.get('category')
        objListing.save()

        return HttpResponseRedirect(reverse("activelisting"))
    
    else:
        return render(request, "auctions/createlisting.html")

@login_required(login_url='/login')
def addtowatchlist(request, product_id):

    obj = Watchlist.objects.filter(listingid = product_id, user = request.user.username)

    if obj:
        obj.delete()

    else:
        obj = Watchlist()
        obj.user = request.user.username
        obj.listingid = product_id
        obj.save()

    return HttpResponseRedirect(reverse("activelisting"))

@login_required(login_url='/login')
def watchlist(request):
    if Watchlist.objects.filter(user = request.user.username) == None:
        return render(request, "auctions/watchlist.html", {
            "empty": empty
        })
    else:
        obj = Watchlist.objects.filter(user = request.user.username)
        products = []
        for items in obj:
            products.append(Listing.objects.get(id=items.listingid))

        if products:
            empty = False
        
        else:
            empty = True

        return render(request, "auctions/watchlist.html", {
            "products": products,
            "empty": empty
        })

@login_required(login_url='/login')
def addcomment(request, product_id):
    if request.method == "POST":

        objComments = Comments()
        objComments.user = request.user.username   
        objComments.comment = request.POST.get('content')
        objComments.listingid = product_id
        objComments.save()

        return HttpResponseRedirect(reverse('viewlisting', kwargs={'product_id':product_id}))
    
    else:
        return HttpResponseRedirect(reverse("activelisting"))

@login_required(login_url='/login')
def closeauction(request, product_id):
    if request.method == "POST":
        objListing = Listing.objects.get(id=product_id)

        allBid = Bid.objects.filter(listingid=product_id)
        objBid = allBid.last()

        objClose = ClosedListings()
        objClose.seller = objListing.seller
        objClose.winner = objBid.user
        objClose.title = objListing.title
        objClose.price = objBid.bid_amount
        objClose.save()

        objWatchlist = Watchlist.objects.filter(listingid=product_id)
        objWatchlist.delete()
        objListing.delete()

        return HttpResponseRedirect(reverse("closedlistings"))
    else:
        return HttpResponseRedirect(reverse("activelisting"))

@login_required(login_url='/login')
def closedlistings(request):
    products = ClosedListings.objects.all()
    empty = False
    if len(products) == 0:
        empty = True
    return render(request, "auctions/closedlistings.html", {
        "products": products,
        "empty": empty
    })

@login_required(login_url='/login')
def categories(request):
    if request.method == "POST":
        products = Listing.objects.filter(category=request.POST.get('cat'))
        empty = False
        if len(products) == 0:
            empty = True
        return render(request, "auctions/categories.html", {
            "start": False,
            "products": products,
            "empty": empty
        })
    else: 
        return render(request, "auctions/categories.html", {
        "start": True
        })