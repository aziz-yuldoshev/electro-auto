from django.db import models
from django.contrib.auth.models import User


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Brend'
        verbose_name_plural = 'Brendlar'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'

    def __str__(self):
        return self.name


class Car(models.Model):
    STATUS_CHOICES = [
        ('available', 'Mavjud'),
        ('reserved', 'Band qilingan'),
        ('sold', 'Sotilgan'),
        ('coming_soon', 'Tez orada'),
    ]

    DRIVE_CHOICES = [
        ('fwd', 'Oldi tortuvchi'),
        ('rwd', 'Orqa tortuvchi'),
        ('awd', '4x4 / AWD'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='cars')
    model = models.CharField(max_length=150)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField()
    battery_capacity = models.DecimalField(max_digits=8, decimal_places=2, help_text='kWh')
    range_km = models.PositiveIntegerField(help_text='km')
    power_hp = models.PositiveIntegerField(help_text='HP')
    torque_nm = models.PositiveIntegerField(help_text='Nm')
    acceleration = models.DecimalField(max_digits=4, decimal_places=2, help_text='0-100 km/h, sekund')
    top_speed = models.PositiveIntegerField(help_text='km/h')
    drive_type = models.CharField(max_length=10, choices=DRIVE_CHOICES)
    charging_time = models.CharField(max_length=100, blank=True)
    charging_power = models.PositiveIntegerField(help_text='kW')
    length = models.PositiveIntegerField(help_text='mm')
    width = models.PositiveIntegerField(help_text='mm')
    height = models.PositiveIntegerField(help_text='mm')
    weight = models.PositiveIntegerField(help_text='kg')
    trunk_capacity = models.PositiveIntegerField(help_text='L')
    main_image = models.ImageField(upload_to='cars/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Avtomobil'
        verbose_name_plural = 'Avtomobillar'

    def __str__(self):
        return f'{self.brand.name} {self.model} ({self.year})'

    @property
    def full_name(self):
        return f'{self.brand.name} {self.model}'


class CarImage(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ImageField(
        upload_to='cars/gallery/'
    )
    title = models.CharField(
        max_length=100,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.car.full_name} - Gallery"


class Favorite(models.Model):
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='favorite_cars'
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')
        ordering = ['-created_at']
        verbose_name = 'Sevimli avtomobil'
        verbose_name_plural = 'Sevimli avtomobillar'

    def __str__(self):
        return f'{self.user.username} — {self.car.full_name}'


class TestDrive(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('confirmed', 'Tasdiqlandi'),
        ('completed', 'Yakunlandi'),
        ('cancelled', 'Bekor qilindi'),
    ]

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='test_drives'
    )

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='test_drives'
    )

    full_name = models.CharField(
        max_length=150,
        verbose_name='Ism va familiya'
    )

    phone = models.CharField(
        max_length=30,
        verbose_name='Telefon'
    )

    date = models.DateField(
        verbose_name='Sana'
    )

    time = models.TimeField(
        verbose_name='Vaqt'
    )

    message = models.TextField(
        blank=True,
        verbose_name='Izoh'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Holat'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yuborilgan vaqt'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Test Drive'
        verbose_name_plural = 'Test Drive arizalari'

    def __str__(self):
        return f'{self.full_name} — {self.car.full_name} — {self.date}'


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Yangi'),
        ('processing', 'Ko‘rib chiqilmoqda'),
        ('confirmed', 'Tasdiqlandi'),
        ('completed', 'Yakunlandi'),
        ('cancelled', 'Bekor qilindi'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='car_orders',
        verbose_name='Mijoz'
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Avtomobil'
    )

    full_name = models.CharField(
        max_length=150,
        verbose_name='Ism familiya'
    )

    phone = models.CharField(
        max_length=30,
        verbose_name='Telefon'
    )

    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name='Izoh'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Holat'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Buyurtma sanasi'
    )

    def __str__(self):
        return f"{self.full_name} — {self.car}"

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'
        ordering = ['-created_at']