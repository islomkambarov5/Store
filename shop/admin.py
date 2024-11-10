from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):    
    list_display = ['username', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['username']

admin.site.register([Category, Product, Order])

