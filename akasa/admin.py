# akasa/admin.py
from django.contrib import admin
from .models import Item, Order, CartItem

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(CartItem)