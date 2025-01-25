from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'is_active', 'is_staff', 'is_superuser', 'telegram_id', 'role']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'role']
    list_editable = ['telegram_id']
    search_fields = ['username', 'email']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'telegram_id', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'telegram_id', 'role',
                       'is_active', 'is_staff', 'is_superuser'),
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity', 'category', 'price', 'creator']
    list_editable = ['quantity', 'price']
    list_display_links = ['name']
    list_filter = ['category', 'creator']
    search_fields = ['name', 'description']
    exclude = ['slug']


admin.site.register([Category, Order])
