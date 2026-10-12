from django.contrib import admin
from .models import Brand, Category, Car, Favorite, TestDrive, CarImage


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'is_active')
    list_filter = ('is_active', 'country')
    search_fields = ('name', 'country')
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'brand',
        'category',
        'year',
        'price',
        'range_km',
        'power_hp',
        'status',
    )

    list_filter = (
        'status',
        'brand',
        'category',
        'drive_type',
        'year',
    )

    search_fields = (
        'model',
        'brand__name',
        'category__name',
    )

    ordering = ('-created_at',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'created_at')
    list_filter = ('created_at',)
    search_fields = (
        'user__username',
        'car__model',
        'car__brand__name',
    )
    ordering = ('-created_at',)


@admin.register(TestDrive)
class TestDriveAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone',
        'car',
        'date',
        'time',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'date',
        'car__brand',
    )

    search_fields = (
        'full_name',
        'phone',
        'car__model',
        'car__brand__name',
    )

    ordering = ('-created_at',)

    readonly_fields = ('created_at',)


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('car', 'title', 'created_at')
    list_filter = ('car__brand',)
    search_fields = ('car__model', 'title')
    ordering = ('-created_at',)