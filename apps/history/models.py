from django.db import models
from decimal import Decimal
import uuid

class OrderHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('online', 'Онлайн'),
        ('split', 'Разделенно'),
    ]
    ORDER_TYPES = [
        ('sale', 'Продажа'),
        ('income', 'Поступление')
        ]
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True)
    shop = models.ForeignKey('product.Shop', on_delete=models.CASCADE, null=True)
    amount = models.FloatField()
    change = models.FloatField(null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, null=True)
    created = models.DateTimeField(auto_now_add=True)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPES, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'История заказа'
        verbose_name_plural = 'История заказа'

    def total_sum(self):
        total = sum((i.quantity * i.amount) for i in self.soldhistory_set.all())
        if total == 0:
            total = sum((i.quantity * i.amount) for i in self.incomehistory_set.all())
        if self.discount:  
            total -= Decimal(self.discount) 
        return total
    
    def total_sum_without_discount(self):
        total = sum((i.quantity * i.amount) for i in self.soldhistory_set.all())
        return total


class SoldHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.ForeignKey('product.Shop', on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(OrderHistory, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'История продаж'
        verbose_name_plural = 'История продаж'

    def total_sum(self):
        return self.quantity * self.amount

    def __str__(self):
        return str(self.id)


class IncomeHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(OrderHistory, on_delete=models.CASCADE, null=True)
    shop = models.ForeignKey('product.Shop', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'История поставки'
        verbose_name_plural = 'История поставки'

    def total_sum(self):
        return self.quantity * self.amount
