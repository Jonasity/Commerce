from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    seller = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.FloatField()
    category = models.CharField(max_length=64)
    image_link = models.CharField(max_length=220, default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)

class Bid(models.Model):
    user = models.CharField(max_length=64)
    bid_amount = models.FloatField()
    title = models.CharField(max_length=64)
    listingid = models.IntegerField()

class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()

class Comments(models.Model):
    user = models.CharField(max_length=64)
    comment = models.TextField()
    listingid = models.IntegerField()
    time = models.DateTimeField(auto_now_add = True)

class ClosedListings(models.Model):
    seller = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    price = models.FloatField()
    winner = models.CharField(max_length=64)