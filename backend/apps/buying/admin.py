from django.contrib import admin
from .models import Item, Order, Discount, Tax, OrderItem

admin.site.register((Item, Order, Discount, Tax, OrderItem))
