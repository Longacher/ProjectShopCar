# serializers.py

from rest_framework import serializers
from .models import Car


class PublicCarSerializer(serializers.ModelSerializer):
    """
    Публичный сериализатор — не раскрывает детали,
    использует маскированные данные из модели.
    """

    class Meta:
        model = Car
        fields = (
            'id',
            'brand',
            'model',
            'year',
            'engine_volume',
            'mileage',
            'engine_type',
            'transmission',
            'drive_type',
            'horsepower',
            'has_accidents',
            'was_taxi',
            'owners_count',
            'price',
            'yearly_maintenance',
            'is_sold'
        )


class MaskedCarSerializer(serializers.Serializer):
    """
    Сериализатор на основе метода модели get_masked_data().
    Используется для безопасной передачи ограниченной информации.
    """

    id = serializers.IntegerField()
    brand = serializers.CharField()
    model = serializers.CharField()
    year = serializers.IntegerField()
    engine_type = serializers.CharField()
    transmission = serializers.CharField()
    drive_type = serializers.CharField()
    horsepower = serializers.IntegerField()
    mileage_masked = serializers.CharField()
    price_masked = serializers.CharField()
    description_masked = serializers.CharField()
    has_accidents = serializers.BooleanField()
    was_taxi = serializers.BooleanField()
    owners_count = serializers.IntegerField()
    is_sold = serializers.BooleanField()


class FullCarSerializer(serializers.ModelSerializer):
    """
    Полный сериализатор — используется только внутри системы.
    Раскрывает все поля автомобиля.
    """

    class Meta:
        model = Car
        fields = '__all__'
