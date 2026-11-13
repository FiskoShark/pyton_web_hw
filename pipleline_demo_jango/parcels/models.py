from django.db import models

class Parcel(models.Model):
    tracking_number = models.CharField(max_length=20, unique=True, verbose_name="Трек-номер")
    recipient_name = models.CharField(max_length=100, verbose_name="Отримувач", default="Невідомий")
    status = models.CharField(max_length=50, default="В обробці", verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    def __str__(self):
        return f"{self.tracking_number} - {self.recipient_name} ({self.status})"
    




