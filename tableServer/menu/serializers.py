from rest_framework import serializers
from .models import Category, Dish, Table, Reservation
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'password')
    def create(self, validated_data):
        return User.objects.create_user(username=validated_data['username'], password=validated_data['password'])

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ('status',)

    def validate(self, data):
        if data['guests_count'] > data['table'].seats:
            raise serializers.ValidationError("Кількість гостей перевищує кількість місць за столиком.")
        
        overlapping = Reservation.objects.filter(
            table=data['table'], date=data['date'], time=data['time']
        ).exclude(status='cancelled')
        if overlapping.exists():
            raise serializers.ValidationError("Цей столик вже заброньований на цей час.")
        return data

