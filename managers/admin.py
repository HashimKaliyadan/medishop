from os import name
from django.contrib import admin
from .models import Category, Medicine
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "in_stock", "is_prescription_required")
    list_filter = ("category", "in_stock", "is_prescription_required")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}