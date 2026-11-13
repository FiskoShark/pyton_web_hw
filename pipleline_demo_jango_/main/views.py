from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Головна сторінка</h1><p>Перевірка middleware.</p>")

def about(request):
    return HttpResponse("<h1>Про нас</h1><p>Тут теж працює middleware.</p>")

def contact(request):
    return HttpResponse("<h1>Контакти</h1><p>І тут теж.</p>")


    