from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'is_active', 'is_staff', 'is_superuser', 'telegram_id']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['username']
    fieldsets = [*UserAdmin.fieldsets]


admin.site.register([Category, Product, Order])
