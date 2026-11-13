from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Parcel

def parcel_list(request):
    parcels = Parcel.objects.all()
    html = "<h1>Список посилок</h1><ul>"
    for p in parcels:
        html += f"<li>{p.tracking_number} - {p.recipient_name} ({p.status})</li>"
    html += "</ul>"
    return HttpResponse(html)

def parcel_detail(request, tracking_number):
    parcel = get_object_or_404(Parcel, tracking_number=tracking_number)
    return HttpResponse(f"<h1>Деталі посилки {parcel.tracking_number}</h1>"
                        f"<p>Отримувач: {parcel.recipient_name}</p>"
                        f"<p>Статус: {parcel.status}</p>")
