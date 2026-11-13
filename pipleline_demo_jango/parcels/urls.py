from django.urls import path
from . import views

urlpatterns = [
    path('', views.parcel_list, name='parcel_list'),
    path('<str:tracking_number>/', views.parcel_detail, name='parcel_detail'),
]



