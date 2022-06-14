from django.contrib import admin
from .models import *
# Register your models here.

class CartFilter(admin.ModelAdmin):
    list_filter = ['isActive']

admin.site.register(Cart, CartFilter)
admin.site.register(CartItem)
