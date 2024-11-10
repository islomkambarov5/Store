from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import requests

# Create your models here.

def send_message(telegram_id, message):
    url = f"https://api.telegram.org/bot6585553255:AAGmt0QI7ag-J2if0FiYTeg4a1aau5UPMzg/sendMessage"
    payload = {
        'chat_id': telegram_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        SELF = 'SELF', 'Self'
        ADMIN = 'ADMIN', 'Admin'
        CUSTOMER = 'CUSTOMER', 'Customer'

    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.SELF)
    is_active = models.BooleanField(default=False)
    telegram_id = models.BigIntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.telegram_id:
            try:
                send_message(self.telegram_id, f"Welcome to our store {self.username}!")
            except Exception as e:
                raise ValueError(f"Failed to send message: {e}")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-id']

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category name')
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['-id']


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Product name')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    quantity = models.IntegerField(verbose_name='Quantity')
    description = models.TextField(verbose_name='Description')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-id']

class Order(models.Model):
    class Statuses(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SOLD = 'SOLD', 'Sold'
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='User')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.IntegerField(verbose_name='Quantity')
    status = models.CharField(max_length=10, choices=Statuses.choices, default=Statuses.PENDING, verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    def __str__(self):
        return f'{self.user} - {self.product}'
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-id']




"""
class CustomUser(AbstractUser):
    first_name, last_name, role, is_active=boolean(default=False), telegram_id

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category name')

class Products(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='User')
    name = models.CharField(max_length=255, verbose_name='Product name')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    quantity = models.IntegerField(verbose_name='Quantity')

class Statuses(models.Model):
    name = models.CharField(max_length=255, verbose_name='Status name')


class Order(models.Model):
    products = models.Foreignkey(Products, on_delete=models.CASCADE, verbose_name='Products')
    quantity = models.IntegerField(verbose_name='Quantity')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    status = models.ForeignKey(Statuses, on_delete=models.CASCADE, verbose_name='Status'),
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
"""

