from django.urls import path
from .views import (
    CategoryListView, DishListCreateView, DishDetailView,
    RegisterView, TableListView, ReservationListCreateView,
    ReservationDetailView, ReservationStatusUpdateView, ReservationCancelView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('dishes/', DishListCreateView.as_view(), name='dish-list-create'),
    path('dishes/<int:pk>/', DishDetailView.as_view(), name='dish-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tables/', TableListView.as_view(), name='table-list'),
    path('reservations/', ReservationListCreateView.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),
    path('reservations/<int:pk>/status/', ReservationStatusUpdateView.as_view(), name='reservation-status'),
    path('reservations/<int:pk>/cancel/', ReservationCancelView.as_view(), name='reservation-cancel'),
]
