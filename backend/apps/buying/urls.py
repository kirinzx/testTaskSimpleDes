from django.urls import path
from .views import BuyItemApiView, MakeOrderApiView, RetrieveBuyingHtmlApiView, RetrieveOrderHtmlApiView

urlpatterns = [
    path('buy/<int:pk>/currency/<str:currency>', BuyItemApiView.as_view()),
    path('item/<int:pk>/currency/<str:currency>',
         RetrieveBuyingHtmlApiView.as_view()),
    path('makeorder/<int:pk>/currency/<str:currency>',
         MakeOrderApiView.as_view()),
    path('order/<int:pk>/currency/<str:currency>',
         RetrieveOrderHtmlApiView.as_view())
]
