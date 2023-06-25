from django.db import models
from django.contrib.auth.models import User
from shop.models import *


class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=32, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    products_price = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.products_price:
            self.products_price = self.product.price * self.amount
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.name