from django.db import models
from datetime import datetime

# comment
class Shop(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='shops', verbose_name='Изображение')
    name = models.CharField(max_length=100, verbose_name='Название')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин', null=True)
    category = models.ForeignKey('product.Category', on_delete=models.SET_NULL, verbose_name='Категория', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name='Продажная цена'
    )
    UNITS = [
        ('шт', 'шт'),
        ('кг', 'кг'),
    ]
    unit = models.CharField(max_length=2, choices=UNITS, default='шт', verbose_name='Единица измерения', null=True)
    image = models.ImageField(null=True, blank=True, upload_to='products', verbose_name='Изображение')
    bar_code = models.CharField(max_length=100, null=True, verbose_name='Штрихкод', unique=True)
    quantity = models.IntegerField(default=0, verbose_name='Количество')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name

    def in_stock(self):
        return self.quantity > 0
    

    def month_sales(self):
        return sum(i.quantity for i in self.soldhistory_set.filter(created__year=datetime.now().year, created__month=datetime.now().month))

class Category(models.Model):
    parent = models.ForeignKey(
        'self',  # Указывает на ту же модель
        on_delete=models.SET_NULL,  # Если родительская категория удалена, поле parent станет NULL
        null=True,  # Родительская категория необязательна
        blank=True,  # Разрешить оставить поле пустым в формах
        related_name='children',  # Удобное имя для доступа к дочерним категориям
        verbose_name='Родитель'
    )
    name = models.CharField(max_length=255, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name