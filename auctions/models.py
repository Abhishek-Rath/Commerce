from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django import forms
import datetime

class User(AbstractUser):
    pass

class Auctions(models.Model):
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "user")  # owner
    title = models.CharField(max_length = 25)
    description = models.CharField(max_length = 200)
    start_bid = models.IntegerField()
    category = models.ForeignKey('Category', on_delete = models.CASCADE, related_name = 'category_for_the_auction', default = 1)
    image = models.ImageField(upload_to = 'images/')
    date = models.DateField(default = timezone.now)
    closed = models.BooleanField(default = False)
    bid = models.ManyToManyField('Bid', blank = True, related_name = "bids")
    last_bid = models.ForeignKey('Bid', on_delete = models.CASCADE, related_name = 'last_bid_for_the_auction', blank = True, null = True)

    def __str__(self):
        return f"{self.title}'s bidding starts at ${self.start_bid}: {self.image}"
        

class Bid(models.Model):
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "bids")
    bid = models.IntegerField()
    date = models.DateField(default = timezone.now)

class Comments(models.Model):
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "user_who_comments")
    auction = models.ForeignKey('Auctions', on_delete = models.CASCADE, related_name = "comments", default = None) # for particular auction's comments
    comment = models.CharField(max_length = 255)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.user} commented {self.comment} on {self.auction}"

class Watchlist(models.Model):
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "watchlist")  # for particular user's watchlist
    auction = models.ForeignKey('Auctions', on_delete = models.CASCADE)

class Category(models.Model):
    category = models.CharField(max_length = 30)   # category for listings

    def __str__(self):
        return self.category

class AuctionsForm(ModelForm):
    class Meta:
        model = Auctions
        fields = ['title', 'description', 'start_bid', 'category', 'image', 'date']
        widgets = {'category' : forms.Select(choices = Category.objects.all(), attrs={'class' : 'form-control'}),
                   'title': forms.TextInput(attrs = {'class': 'form-control'}),
                   'description': forms.TextInput(attrs = {'class': 'form-control'}),
                   'start_bid': forms.NumberInput(attrs = {'class': 'form-control'}),} 

class BidForm(ModelForm):
    '''Django form for bid model '''
    class Meta:
        model = Bid
        fields = ['bid']
        widgets = {'bid' : forms.NumberInput(attrs = {'class' : 'form-control'})}

class CommentsForm(ModelForm):
    '''Django form for comment model '''
    class Meta:
        model = Comments
        fields = ['comment']
        widgets = {'comment' : forms.TextInput(attrs = {'class' : 'form-control'})}
