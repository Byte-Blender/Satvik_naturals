from django.contrib import admin
from .models import Category, Product, CreativeUse

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CreativeUse)
class CreativeUseAdmin(admin.ModelAdmin):
    list_display = ['title', 'emoji', 'is_active', 'order']
    list_editable = ['is_active', 'order']
