# admin.py
from django.contrib import admin
from .models import InventoryItem, Category
from .forms import InventoryItemForm

class InventoryItemAdmin(admin.ModelAdmin):
    form = InventoryItemForm
    list_display = ('name', 'user', 'category', 'department', 'condition', 'date_created')
    list_filter = ('user', 'category', 'department', 'condition', 'date_created')
    search_fields = ('name', 'specifications', 'location', 'user__username')

admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(Category)
