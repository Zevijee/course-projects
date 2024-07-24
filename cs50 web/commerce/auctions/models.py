from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

from .choices import CATEGORY_CHOICES

def MinValueValidator(value):
    if value <= 0.00:
        raise ValidationError('Starting bid must be greater than or equal to 0.01')

class User(AbstractUser):
    pass

class Listing(models.Model):
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    current_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.01, validators=[MinValueValidator])
    category = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='listings/', blank=True, null=True)
    closed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings_won', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"item {self.id} {self.title}"

class Watchlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listings = models.ManyToManyField(Listing, related_name='watchlists')

    def add_listing(self, listing):
        self.listings.add(listing)

    def remove_listing(self, listing):
        self.listings.remove(listing)

    def get_listings(self):
        return self.listings.all()

    def __str__(self):
        return f"{self.owner.username}'s watchlist"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bid')
    bid = models.DecimalField(max_digits=8, decimal_places=2, default=0.01)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.bidder.username} on {self.listing.title}"

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(max_length=2000, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment by {self.commenter.username} on {self.listing.title}"