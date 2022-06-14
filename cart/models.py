from asyncio.windows_events import NULL
from itertools import product
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from watch.models import Watch
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateFinished = models.DateTimeField(blank=True, null=True)
    total = models.DecimalField(default=0, decimal_places=2, max_digits=12)

    @classmethod
    def create(cls, user1):
        Cart = cls(user = user1)
        return Cart

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Watch, on_delete=models.CASCADE)

    @classmethod
    def create(cls, cart1, product1):
        CartItem = cls(cart = cart1, product = product1)
        return CartItem


