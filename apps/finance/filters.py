import django_filters
from .models import *
from django import forms


class ExpenseFilter(django_filters.FilterSet):
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
    expend_type = django_filters.ChoiceFilter(
        choices=Expense.EXPENSE_TYPES,
        widget=forms.widgets.Select(
            attrs={
                'class': 'form-select'
            }
        ), label='Тип расхода'
    )
