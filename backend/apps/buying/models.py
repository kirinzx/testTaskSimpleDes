from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField(min_value=0.0)


class Discount(models.Model):
    promo_code = models.CharField(max_length=255)
    discount_percents = models.FloatField(min_value=0.0)


class Tax(models.Model):
    name = models.CharField(max_length=255, unique=True)
    tax_percents = models.FloatField(min_value=0.0)


class Order(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT)
    tax = models.ForeignKey(Tax, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
