from django.contrib import admin

from .models import (
    Basket,
    Category,
    Favorite,
    Products,
    ProductsGallery,
    Profile,
    Slider,
)


# Register your models here.
class ProductsGalleryInline(admin.TabularInline):
    model = ProductsGallery


class ProductsAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "category", "price", "author"]
    list_display_links = ["pk", "name"]
    inlines = [ProductsGalleryInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    list_display_links = ["pk", "name"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Slider)
admin.site.register(Basket)
admin.site.register(Favorite)
admin.site.register(Profile)
