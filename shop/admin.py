from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "category", "price", "stock", "available")
    list_filter = ("category", "available")
    search_fields = ("name", "brand")
    prepopulated_fields = {"slug": ("name",)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "unit_price", "quantity")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "email", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("email", "full_name")
    inlines = [OrderItemInline]
