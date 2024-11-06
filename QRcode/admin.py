from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'username', 'role', 'joined_at')
    list_filter = ('joined_at', 'role')
    search_fields = ('full_name', 'username')
    date_hierarchy = 'joined_at'


@admin.register(QrCode)
class QrCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', "created_at")
    list_filter = ('is_active', 'created_at')
    search_fields = ('information',)
    date_hierarchy = 'created_at'