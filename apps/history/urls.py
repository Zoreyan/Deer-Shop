from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # История
    path('total/', total, name='total'),
    path('sold-history/', sales, name='sold-history'),
    path('income-history/', incomes, name='income-history'),
    path('sold-history-delete/<uuid:pk>/', sales_delete, name='sold-history-delete'),
    path('income-history-delete/<uuid:pk>/', income_delete, name='income-history-delete'),
    path('order-history-delete/<uuid:pk>/', order_delete, name='order-history-delete'),
    path('receipt/<int:pk>/', receipt, name='receipt'),
]