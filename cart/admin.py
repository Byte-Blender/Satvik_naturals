from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ['product', 'quantity']
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]