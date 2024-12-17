# inventory/admin.py

from django.contrib import admin
from .models import Equipment, CheckoutRequest

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('asset_number', 'model_number', 'price', 'due_date', 'checked_out_to')
    search_fields = ('asset_number', 'model_number', 'checked_out_to__username', 'due_date')

@admin.register(CheckoutRequest)
class CheckoutRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'equipment', 'use_case', 'date_needed_until', 'status')
    search_fields = ('user__username', 'equipment__asset_number', 'status')
