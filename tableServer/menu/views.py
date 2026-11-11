
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Category, Dish, Table, Reservation
from .serializers import (
    CategorySerializer, DishSerializer, 
    RegisterSerializer, TableSerializer, ReservationSerializer
)
from django.contrib.auth.models import User

# --- МЕНЮ ---
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DishListCreateView(generics.ListCreateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class DishDetailView(generics.RetrieveAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

# --- РЕЄСТРАЦІЯ ТА СТОЛИКИ ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class TableListView(generics.ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = (permissions.AllowAny,)

# --- БРОНЮВАННЯ ---
class ReservationListCreateView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReservationDetailView(generics.RetrieveAPIView):
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

class ReservationStatusUpdateView(generics.UpdateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['patch', 'put']

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get('status')
        if new_status not in ['confirmed', 'completed']:
            return Response({"error": "Можна змінити статус тільки на 'confirmed' або 'completed'"}, status=status.HTTP_400_BAD_REQUEST)
        instance.status = new_status
        instance.save()
        return Response(self.get_serializer(instance).data)

class ReservationCancelView(generics.DestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)
    def perform_destroy(self, instance):
        instance.status = 'cancelled'
        instance.save()


def index(request):
    return render(request, 'menu/index.html')

