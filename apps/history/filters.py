import django_filters
from .models import *
from django import forms

class OrderHistoryFilter(django_filters.FilterSet):

    created_min = django_filters.DateTimeFilter(
        field_name="created", lookup_expr="gte",
        label="Дата от",
        widget= forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
    created_max = django_filters.DateTimeFilter(
        field_name="created", lookup_expr="lte",
        label="Дата до",
        widget= forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
    payment_method = django_filters.ChoiceFilter(
        choices=OrderHistory.PAYMENT_METHODS,
        widget=forms.widgets.Select(
            attrs={
                'class': 'form-select'
            }
        ), label='Метод оплаты'
    )
  
    amount_min = django_filters.NumberFilter(
        field_name="amount", lookup_expr="gte",
        label="Цена от",
        widget= forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена от:'})
    )
    amount_max = django_filters.NumberFilter(
        field_name="amount", lookup_expr="lte",
        label="Цена до",
        widget= forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена до:'})
    )


class SoldHistoryFilter(django_filters.FilterSet):

    created_min = django_filters.DateTimeFilter(
        field_name="created", lookup_expr="gte",
        label="Дата от",
        widget= forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
    created_max = django_filters.DateTimeFilter(
        field_name="created", lookup_expr="lte",
        label="Дата до",
        widget= forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
    amount_min = django_filters.NumberFilter(
        field_name="amount", lookup_expr="gte",
        label="Цена от",
        widget= forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена от:'})
    )
    amount_max = django_filters.NumberFilter(
        field_name="amount", lookup_expr="lte",
        label="Цена до",
        widget= forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена до:'})
    )
    quantity_min = django_filters.NumberFilter(
        field_name="quantity", lookup_expr="gte",
        label="Кол-во от",
        widget= forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Кол-во от:'})
    )
    quantity_max = django_filters.NumberFilter(
        field_name="quantity", lookup_expr="lte",
        label="Кол-во до",
        widget= forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Кол-во до:'})
    )


class IncomeHistoryFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(
        field_name="product__name", lookup_expr="icontains",
        label="Название товара",
        widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название товара:'})
    )

    created_min = django_filters.DateTimeFilter(
        field_name="created", lookup_expr="gte",
        label="Дата от",
        widget= forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
    created_max = django_filters.DateTimeFilter(
        field_name="created", lookup_expr="lte",
        label="Дата до",
        widget= forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
    amount_min = django_filters.NumberFilter(
        field_name="amount", lookup_expr="gte",
        label="Цена от",
        widget= forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена от:'})
    )
    amount_max = django_filters.NumberFilter(
        field_name="amount", lookup_expr="lte",
        label="Цена до",
        widget= forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена до:'})
    )
    quantity_min = django_filters.NumberFilter(
        field_name="quantity", lookup_expr="gte",
        label="Кол-во от",
        widget= forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Кол-во от:'})
    )
    quantity_max = django_filters.NumberFilter(
        field_name="quantity", lookup_expr="lte",
        label="Кол-во до",
        widget= forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Кол-во до:'})
    )


class LogHistoryFilter(django_filters.FilterSet):

    created_min = django_filters.DateTimeFilter(
        field_name="created", lookup_expr="gte",
        label="Дата от",
        widget= forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
    created_max = django_filters.DateTimeFilter(
        field_name="created", lookup_expr="lte",
        label="Дата до",
        widget= forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )

    message = django_filters.CharFilter(
        field_name="message", lookup_expr="icontains",
        label="Сообщение",
        widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Сообщение:'})
    )