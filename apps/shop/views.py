from django.shortcuts import render
from apps.product.models import Shop, Product, Category
# Create your views here.


def index(request, pk):
    shop = Shop.objects.get(id=pk)
    products = Product.objects.filter(shop=shop)
    categories = Category.objects.filter(shop=shop)
    context = {
        'shop': shop,
        'products': products,
        'categories': categories
    }
    return render(request, 'shop/index.html', context)


def about_us(request, pk):
    shop = Shop.objects.get(id=pk)
    context = {
        'shop': shop
    }
    return render(request, 'shop/about_us.html', context)


def contacts(request, pk):
    shop = Shop.objects.get(id=pk)
    context = {
        'shop': shop
    }
    return render(request, 'shop/contacts.html', context)


def vacancies(request, pk):
    shop = Shop.objects.get(id=pk)
    context = {
        'shop': shop
    }
    return render(request, 'shop/vacancies.html', context)


def order_list(request):
    context = {
    }
    return render(request, 'shop/order_list.html', context)