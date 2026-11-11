from django.contrib import admin
from .models import Category, Dish, Table, Reservation

admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Table)
admin.site.register(Reservation)


