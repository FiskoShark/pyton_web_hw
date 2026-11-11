from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=150, verbose_name="Назва страви")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")
    category = models.ForeignKey(Category, related_name='dishes', on_delete=models.CASCADE, verbose_name="Категорія")
    available = models.BooleanField(default=True, verbose_name="Доступність")

    def __str__(self):
        return self.name


# ---  ---

class Table(models.Model):
    number = models.PositiveIntegerField(unique=True, verbose_name="Номер столика")
    seats = models.PositiveIntegerField(verbose_name="Кількість місць")
    is_available = models.BooleanField(default=True, verbose_name="Доступність")

    def __str__(self):
        return f"Столик {self.number} ({self.seats} місць)"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує підтвердження'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
        ('completed', 'Завершено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', verbose_name="Користувач")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations', verbose_name="Столик")
    date = models.DateField(verbose_name="Дата бронювання")
    time = models.TimeField(verbose_name="Час")
    guests_count = models.PositiveIntegerField(verbose_name="Кількість гостей")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Столик {self.table.number} на {self.date} {self.time}"

    
