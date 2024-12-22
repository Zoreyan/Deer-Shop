from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
from apps.history.models import *
from apps.finance.models import *
from django.forms.models import model_to_dict
import json
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q

def update_product_per_page(request):
    if request.method == "POST":
        try:
            items_per_page = int(request.POST.get("items_per_page", 10))
            if items_per_page > 0:
                request.session['items_per_page'] = items_per_page
        except ValueError:
            request.session['items_per_page'] = 10  # Устанавливаем значение по умолчанию
    return redirect('settings') 


def list_(request):
    products = Product.objects.all()

    categories = Category.objects.all()

    query = request.GET.get('query', '').strip()

    if query:
        if query.isdigit():
            products = products.filter(shop=request.user.shop, bar_code__icontains=query)
        else:
            products = products.filter(
                Q(shop=request.user.shop) & 
                (Q(name__icontains=query) | Q(category__name__icontains=query))
            )         
    # Фильтр по категории и родительской категории
    selected_category = request.GET.get('category')
    if selected_category:
        # Получаем выбранную категорию
        category = Category.objects.filter(name=selected_category).first()

        # Продукты из выбранной категории
        category_products = products.filter(category=category)

        # Продукты из дочерних категорий
        child_categories = category.children.all() if category else []
        child_category_products = products.filter(category__in=child_categories)

        # Объединяем и сортируем продукты
        products = list(category_products) + list(child_category_products)

    # Фильтр по минимальной сумме
    price_min = request.GET.get('price_min')
    if price_min:
        products = products.filter(price__gte=price_min)

    # Фильтр по максимальной сумме
    price_max = request.GET.get('price_max')
    if price_max:
        products = products.filter(price__lte=price_max)

    # Фильтр по наличию
    in_stock = request.GET.get('in_stock')
    if in_stock == "yes":
        products = products.filter(quantity__gt=0)
    elif in_stock == "no":
        products = products.filter(quantity=0)

    # Для пагинации
    items_per_page = request.session.get('items_per_page', 10)
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Ограничение отображаемых страниц
    current_page = page_obj.number
    total_pages = paginator.num_pages
    delta = 3  # Количество страниц до и после текущей

    start_page = max(current_page - delta, 1)
    end_page = min(current_page + delta, total_pages)
    visible_pages = range(start_page, end_page + 1)

    context = {
        'categories': categories,
        'visible_pages': visible_pages,
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'product/list.html', context)


def create(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.shop = request.user.shop
            form.save()
            messages.success(request, 'Товар успешно создан')
            return redirect('product-create')
        else:
            messages.error(request, 'Ошибка при создании товара')
    return render(request, 'product/create.html', {'form': form})

def product_create(request):
    # Проверяем, что запрос является AJAX и имеет метод POST
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Преобразуем данные JSON из запроса
        data = json.loads(request.body)
        
        # Создаем объект Product с полученными данными и значениями по умолчанию
        product = Product(
            name=data.get('name'),
            bar_code=data.get('barcode'),
            price=data.get('price', 0),       # Цена по умолчанию 0
            quantity=data.get('quantity', 0), # Количество по умолчанию 0
            sale_price=data.get('sale_price', 0), # Продажная цена по умолчанию 0
            shop=request.user.shop
        )

        # Сохраняем объект и возвращаем ответ JSON
        try:
            product.save()
            return JsonResponse({'success': True, 'barcode': product.bar_code})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def details(request, pk):
    product = Product.objects.get(id=pk)

    context = {
        'product': product,
    }
    return render(request, 'product/details.html', context)


def update(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-list')

    context = {
        'product': product,
        'form': form
    }
    return render(request, 'product/update.html', context)


def delete(request, pk):
    Product.objects.get(id=pk).delete()
    return redirect('product-list')


def sale(request):
    return render(request, 'product/sale.html')

def income(request):
    return render(request, 'product/income.html')


def get_product(request):
    bar_code = request.GET.get('bar_code')
    product = get_object_or_404(Product, bar_code=bar_code)

    product = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'sale_price': product.sale_price,
        'bar_code': product.bar_code,
        'quantity': product.quantity,
        'status': 'success' if product is not None else 'error',
    }

    return JsonResponse(product, safe=False)


def create_sell_history(request):
    if request.method == 'POST':
        products = json.loads(request.POST.get('products'))
        amount = request.POST.get('amount')
        change = request.POST.get('change')
        discount = request.POST.get('discount')

        profit = Decimal(0)

        if discount == '':
            discount = 0

        order = OrderHistory.objects.create(
            shop=request.user.shop,
            amount=amount,
            change=change,
            discount=discount,
        )
        for item in products:
            product = Product.objects.get(id=item['id'])
            quantity = int(item['quantity'])

            # Проверяем доступность количества
            if product.quantity < quantity:
                return JsonResponse({
                    'status': 'error',
                    'message': f"Недостаточно товара для продукта {product.name}. Доступно: {product.quantity}, запрошено: {quantity}."
                })

            # Сохраняем текущую цену продукта
            SoldHistory.objects.create(
                shop=request.user.shop,
                order=order,
                product=product,
                quantity=quantity,
                price_at_moment=product.sale_price
            )

            product_profit = (Decimal(product.sale_price) - Decimal(product.price)) * quantity
            profit += product_profit


            # Обновляем количество продукта
            product.quantity -= quantity
            product.save()
        
        profit = profit - Decimal(discount)

        order.profit = profit
        order.save()

        return JsonResponse({'status': 'success'})
        
        

def create_income_history(request):
    if request.method == 'POST':
        products = json.loads(request.POST.get('products'))
        amount = request.POST.get('amount')
        change = request.POST.get('change')
        change = request.POST.get('change')

        # Создаем запись о поступлении
        order = OrderHistory.objects.create(
            amount=amount,
            change=change,
            shop=request.user.shop
        )
        expend = Expense.objects.create(
            expend_type='supplies',
            description='Поступление',
            amount=amount,
            shop=request.user.shop,
        )

        for item in products:
            product = Product.objects.get(id=item['id'])
            quantity = int(item['quantity'])
            price = float(item['price'])  # Получаем цену продукта из запроса
            sale_price = float(item['sale_price'])  # Получаем продажную цену из запроса

            
            IncomeHistory.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_moment=price,
                shop=request.user.shop
            )

            # Обновляем количество и цены продукта
            product.quantity += quantity
            product.price = price  # Обновляем цену
            product.sale_price = sale_price  # Обновляем продажную цену
            product.save()

        return JsonResponse({'status': 'success'})


def update_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        product = Product.objects.get(id=product_id)
        product.quantity = quantity
        product.save()

        return JsonResponse({'status': 'success'})


def find_product(request):
    barcode = request.GET.get('barcode')
    try:
        product = Product.objects.get(bar_code=barcode, shop=request.user.shop)
        return JsonResponse({'product_name': product.name, 'price': product.price, 'image': product.image.url})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


def search_product(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query).values('bar_code', 'name', 'quantity')
    return JsonResponse(list(products), safe=False)



def category_list(request):
    categories = Category.objects.annotate(total_products=Count('product'))
    form = CategoryForm()   

    # Пагинация
    category_per_page = request.session.get('category_per_page', 10)
    paginator = Paginator(categories, category_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Ограничение отображаемых страниц
    current_page = page_obj.number
    total_pages = paginator.num_pages
    delta = 3  # Количество страниц до и после текущей

    start_page = max(current_page - delta, 1)
    end_page = min(current_page + delta, total_pages)
    visible_pages = range(start_page, end_page + 1)

    context = {
        'page_obj': page_obj,
        'visible_pages': visible_pages,
        'form': form,
    }
    return render(request, 'product/category_list.html', context)

def update_category_per_page(request):
    if request.method == "POST":
        try:
            category_per_page = int(request.POST.get("category_per_page", 10))
            if category_per_page > 0:
                request.session['category_per_page'] = category_per_page
        except ValueError:
            request.session['category_per_page'] = 10
    return redirect('settings')

def category_create(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-list')

    context = {
        'form': form
    }
    return render(request, 'product/category_create.html', context)

def category_delete(request, pk):
    if request.method == 'POST':
        category = Category.objects.get(id=pk)
        category.delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

def category_update(request, pk):
    category = Category.objects.get(id=pk)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-list')

    context = {
        'category': category,
        'form': form
    }