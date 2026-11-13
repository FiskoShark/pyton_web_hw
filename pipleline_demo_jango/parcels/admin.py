from django.contrib import admin
from .models import Parcel

@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'recipient_name', 'status', 'created_at')
    search_fields = ('tracking_number', 'recipient_name')




    