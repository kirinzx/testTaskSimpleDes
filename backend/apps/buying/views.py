from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Item, Order, OrderItem
import stripe
from stripe.error import InvalidRequestError
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.conf import settings
import json
from django.http import JsonResponse


class BuyItemApiView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk=None, currency=None):
        currency = currency.upper()

        if currency not in settings.CURRENCIES:
            return Response(data={"detail": "Неизвестная валюта"}, status=status.HTTP_400_BAD_REQUEST)

        item: Item = get_object_or_404(Item, pk=pk)

        item_price = float(item.price_currency.get(currency))
        try:
            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'unit_amount': int(item_price * 100),
                        'product_data': {
                            'name': item.name,
                            'description': item.description
                        },
                        'currency': currency
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'http://127.0.0.1:8000/buy/{pk}/currency/{currency}',
            )
        except InvalidRequestError:
            return Response(data={"detail": "Ошибка в запросе к Stripe"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={"session_id": session.id})


class RetrieveBuyingHtmlApiView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)

    def get(self, request, pk=None, currency=None):
        item: Item = get_object_or_404(Item, pk=pk)
        currency = currency.upper()
        if currency not in settings.CURRENCIES:
            return Response(data={'detail': 'Неизвестная валюта'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'currency': currency, 'item': item}, template_name="buying.html", content_type='text/html')


class MakeOrderApiView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk=None, currency=None):
        currency = currency.upper()

        if currency not in settings.CURRENCIES:
            return Response(data={"detail": "Неизвестная валюта"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.filter(
            pk=pk)

        if not order.exists():
            return Response(data={"detail": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)

        orderitems = OrderItem.objects.filter(
            order=pk).prefetch_related('item')

        if not orderitems.exists():
            return Response(data={"detail": "Заказ не содержит товаров"}, status=status.HTTP_400_BAD_REQUEST)

        order = order.select_related(
            'tax', 'discount').get(pk=pk)

        line_items = []

        for orderitem in orderitems:
            item = orderitem.item
            item_price = float(item.price_currency.get(currency))
            line_items.append(
                {
                    'price_data': {
                        'unit_amount': int(item_price * 100),
                        'product_data': {
                            'name': item.name,
                            'description': item.description
                        },
                        'currency': currency,
                    },
                    'quantity': 1,
                    'tax_rates': [order.tax.stripe_id] if order.tax is not None else []
                }
            )
        try:
            session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                success_url=f'http://127.0.0.1:8000/order/',
                discounts=[
                    {
                        'coupon': order.discount.stripe_id if order.discount is not None else None
                    }
                ]
            )

        except InvalidRequestError:
            return Response(data={"detail": "Ошибка в запросе к Stripe"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={"session_id": session.id})


class RetrieveOrderHtmlApiView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)

    def get(self, request, pk=None, currency=None):

        currency = currency.upper()

        if currency not in settings.CURRENCIES:
            return Response(data={"detail": "Неизвестная валюта"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.filter(
            pk=pk)

        if not order.exists():
            return Response(data={"detail": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)

        orderitems = OrderItem.objects.filter(
            order=pk).prefetch_related('item')

        if not orderitems.exists():
            return Response(data={"detail": "Заказ не нсодержит товаров"}, status=status.HTTP_400_BAD_REQUEST)

        order = order.select_related(
            'tax', 'discount').get(pk=pk)

        return Response(data={'currency': currency, 'orderitems': orderitems, 'order': order}, template_name="order.html", content_type='text/html')


def openapi_spec(request):
    with open('apiSpec.json')as f:
        openapi = json.load(f)

    return JsonResponse(openapi, safe=False)
