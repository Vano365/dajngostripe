from tabnanny import verbose
from django.db import models

# Create your models here.
class Item(models.Model):
    cur = (
        ('usd', 'USD'),
        ('eur', 'EUR'),
        ('rub', 'RUB'),
    )
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.IntegerField(verbose_name="Цена")
    currency = models.CharField(max_length=3, choices=cur)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Order(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, verbose_name="Продукт")
    qty = models.IntegerField(verbose_name="Кол-во")

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'