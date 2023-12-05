from django.urls import path
from django.views.generic import TemplateView
from .views import BuyItemApiView, MakeOrderApiView, RetrieveBuyingHtmlApiView, RetrieveOrderHtmlApiView, openapi_spec

urlpatterns = [
    path('buy/<int:pk>/currency/<str:currency>', BuyItemApiView.as_view()),
    path('item/<int:pk>/currency/<str:currency>',
         RetrieveBuyingHtmlApiView.as_view()),
    path('makeorder/<int:pk>/currency/<str:currency>',
         MakeOrderApiView.as_view()),
    path('order/<int:pk>/currency/<str:currency>',
         RetrieveOrderHtmlApiView.as_view()),
    path('openapi_spec', openapi_spec, name='openapi_spec'),
    path('docs/', TemplateView.as_view(
        template_name='swagger-ui.html'
    ), name='swagger-ui'),
]
