from django.db import models
import stripe
from stripe.error import InvalidRequestError
from django.core.exceptions import ValidationError
from django.conf import settings


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_currency = models.JSONField()

    def __str__(self) -> str:
        return f'{self.name}. Id: {self.pk}'

    def clean(self):

        if not isinstance(self.price_currency, dict):
            raise ValidationError(
                'Поле "price_currency" должно быть json объектом'
            )

        currencies = settings.CURRENCIES

        if len(self.price_currency.keys()) != len(currencies):
            raise ValidationError(
                'Поле "price_currence" должно содержать только две валюты: "USD" и "RUB"'
            )

        for currency in currencies:
            price = self.price_currency.get(currency, None)
            if price is None:
                raise ValidationError(
                    f'Цена у валюты "{currency}" в поле "price_currency" обязательный'
                )
            if not (isinstance(price, float) or isinstance(price, int)):
                raise ValidationError(
                    f'Значения ключа "{currency}" в поле "price_currency" должно быть целым или нецелым числом'
                )

            # if price >=

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Discount(models.Model):
    name = models.CharField(max_length=255, unique=True)
    discount_percents = models.DecimalField(max_digits=3, decimal_places=1)
    stripe_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name}. Discount: {self.discount_percents}%'

    def create_coupon(self):
        try:
            coupon = stripe.Coupon.create(
                duration='forever',
                percent_off=self.discount_percents
            )
            self.stripe_id = coupon.id
        except InvalidRequestError:
            raise ValidationError(
                'Ошибка в запросе'
            )

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError(
                "Купон нельзя обновить!"
            )
        self.create_coupon()

        super().save(*args, **kwargs)


class Tax(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    tax_percents = models.DecimalField(max_digits=3, decimal_places=1)
    inclusive = models.BooleanField()
    stripe_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name}. Discount: {self.tax_percents}%'

    def create_tax(self):
        try:
            tax = stripe.TaxRate.create(
                display_name=self.name,
                description=self.description,
                percentage=self.tax_percents,
                inclusive=self.inclusive
            )
            self.stripe_id = tax.id
        except InvalidRequestError:
            raise ValidationError(
                'Ошибка в запросе'
            )

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError(
                'Налог нельзя обновить'
            )
        self.create_tax()
        super().save(*args, **kwargs)


class Order(models.Model):
    discount = models.ForeignKey(
        Discount, on_delete=models.PROTECT, null=True, blank=True)
    tax = models.ForeignKey(
        Tax, on_delete=models.PROTECT, null=True, blank=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'Order: {self.order}. Item: {self.item.name}'
