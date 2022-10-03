from datetime import datetime
from enum import Enum
import enum
from multiprocessing import Value
import uuid
from django.db import models
from django.urls import reverse
import requests

class OrderStatus(Enum):
    PLACED = enum.auto
    CONFIRMED = enum.auto

    def __str__(self) -> str:
        return self.name

class PaymentStatus(Enum):
    UNPAID = enum.auto
    PAID = enum.auto

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product_name = models.CharField(max_length=200)
    image = models.ImageField(blank=True)
    content = models.CharField(max_length=2000)
    price = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.product_name


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product = models.ManyToManyField(Product, blank=True)
    total_price = models.PositiveIntegerField()
    status_str = models.CharField(max_length=50, default=OrderStatus.PLACED , editable=False, verbose_name="Stauts")
    time_created = models.DateTimeField()
    time_confirmed = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.id)

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    order = models.OneToOneField(Order, on_delete=models.PROTECT)
    total = models.IntegerField(editable=False, blank=True, default = 0)
    status_str = models.CharField(default=PaymentStatus.UNPAID, max_length=50, editable=False, verbose_name="Status")
    payment_method = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.payment_method