from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
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

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=60, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    telegram_id = models.BigIntegerField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.SELF)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if the instance is new (create operation)

        if is_new and self.telegram_id:
            try:
                send_message(self.telegram_id, f"Welcome to our store {self.username}!")
            except Exception as e:
                # Log the error and optionally handle it
                print(f"Error sending message: {e}")
                raise ValueError("Please provide a valid telegram_id.")

        # Call the parent class's save method to persist the object
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_active or self.is_superuser


@receiver(post_save, sender=CustomUser)
def send_welcome_or_status_update(sender, instance, created, **kwargs):
    if not instance.telegram_id:
        return  # No telegram ID to send a message to

    try:
        if created:
            send_message(instance.telegram_id, f"Welcome to our store {instance.username}!")
        else:
            if instance.is_active:
                from rest_framework_simplejwt.tokens import RefreshToken
                refresh = RefreshToken.for_user(instance)
                send_message(instance.telegram_id, "Your account has been activated!\n\n"
                                                   f"refresh: {str(refresh)}\n\n"
                                                   f"access: {str(refresh.access_token)}")
            else:
                send_message(instance.telegram_id, "Your account is in a pending state!")
    except Exception as e:
        # Log the error instead of raising an exception
        print(f"Error sending message: {e}")


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
