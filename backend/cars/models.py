from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



class Car(models.Model):
    """Основная модель автомобиля"""

    brand = models.CharField(max_length=50, verbose_name="Марка")
    model = models.CharField(max_length=50, verbose_name="Модель")
    year = models.IntegerField(
        verbose_name="Год выпуска",
        validators=[
            MinValueValidator(1990),
            MaxValueValidator(2024)
        ]
    )
    
    engine_volume = models.PositiveIntegerField(

    )
    engine_type = models.CharField(
        max_length=20,
        choices=[
            ('petrol', 'Бензин'),
            ('diesel', 'Дизель'),
            ('hybrid', 'Гибрид'),
            ('electric', 'Электро'),
            ('gas', 'Газ/Бензин'),
        ],
        verbose_name="Тип двигателя"
    )
    transmission = models.CharField(
        max_length=20,
        choices=[
            ('manual', 'Механическая'),
            ('automatic', 'Автоматическая'),
            ('robot', 'Роботизированная'),
            ('variator', 'Вариатор'),
        ],
        verbose_name="Коробка передач"
    )
    drive_type = models.CharField(
        max_length=20,
        choices=[
            ('front', 'Передний'),
            ('rear', 'Задний'),
            ('all', 'Полный'),
        ],
        verbose_name="Привод"
    )
    horsepower = models.IntegerField(verbose_name="Мощность (л.с.)")
    
    mileage = models.IntegerField(
        verbose_name="Пробег (км)",
        validators=[MinValueValidator(0)]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена (руб)"
    )
    
    owners_count = models.IntegerField(
        verbose_name="Количество владельцев",
        validators=[MinValueValidator(1)],
        default=1
    )
    
    accidents = models.TextField(
        verbose_name="История ДТП",
        blank=True,
        null=True,
        help_text="Описание аварий, если были"
    )
    has_accidents = models.BooleanField(
        verbose_name="Участвовал в ДТП",
        default=False
    )
    
    was_taxi = models.BooleanField(
        verbose_name="Использовался в такси",
        default=False
    )
    taxi_years = models.IntegerField(
        verbose_name="Лет в такси",
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    repair_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Общая стоимость ремонтов (руб)",
        default=0
    )
    yearly_maintenance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Среднее обслуживание в год (руб)",
        help_text="Приблизительная стоимость обслуживания машины в год"
    )

    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    is_sold = models.BooleanField(default=False, verbose_name="Продано")
    
    # Фотографии (через отдельную модель)
    # main_image = models.ImageField(upload_to='cars/', blank=True, null=True, verbose_name="Главное фото")
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['brand', 'model']),
            models.Index(fields=['year']),
            models.Index(fields=['price']),
            models.Index(fields=['mileage']),
        ]
    
    def __str__(self):
        return f"{self.brand} {self.model} {self.year} - {self.price} руб."
    
    @property
    def full_name(self):
        """Полное название автомобиля"""
        return f"{self.brand} {self.model} {self.year}"
    
    @property
    def price_per_year(self):
        """Стоимость года эксплуатации"""
        if self.year:
            age = 2024 - self.year
            if age > 0:
                return self.price / age
        return self.price
    
    @property
    def has_commercial_history(self):
        """Была ли машина в коммерческом использовании"""
        return self.was_taxi or self.taxi_years > 0


class CarImage(models.Model):
    """Модель для фотографий автомобилей"""
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Автомобиль"
    )
    image = models.ImageField(
        upload_to='cars/images/',
        verbose_name="Фотография"
    )
    is_main = models.BooleanField(default=False, verbose_name="Главное фото")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Фотография автомобиля"
        verbose_name_plural = "Фотографии автомобилей"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Фото {self.car}"


class MaintenanceRecord(models.Model):
    """История обслуживания автомобиля"""
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='maintenance_records',
        verbose_name="Автомобиль"
    )
    date = models.DateField(verbose_name="Дата обслуживания")
    service_type = models.CharField(
        max_length=100,
        verbose_name="Вид обслуживания"
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость (руб)"
    )
    description = models.TextField(
        verbose_name="Описание работ",
        blank=True,
        null=True
    )
    mileage_at_service = models.IntegerField(
        verbose_name="Пробег при обслуживании"
    )
    
    class Meta:
        verbose_name = "Запись обслуживания"
        verbose_name_plural = "История обслуживания"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.car} - {self.service_type} - {self.date}"


class CarFeature(models.Model):
    """Дополнительные опции автомобиля"""
    name = models.CharField(max_length=100, verbose_name="Название опции")
    category = models.CharField(
        max_length=50,
        choices=[
            ('comfort', 'Комфорт'),
            ('safety', 'Безопасность'),
            ('multimedia', 'Мультимедиа'),
            ('exterior', 'Экстерьер'),
            ('other', 'Другое'),
        ],
        verbose_name="Категория"
    )
    
    class Meta:
        verbose_name = "Опция автомобиля"
        verbose_name_plural = "Опции автомобилей"
    
    def __str__(self):
        return self.name



class CarFeatures(models.Model):
    """Связь автомобилей с их опциями"""
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='car_features',
        verbose_name="Автомобиль"
    )
    feature = models.ForeignKey(
        CarFeature,
        on_delete=models.CASCADE,
        verbose_name="Опция"
    )
    
    class Meta:
        verbose_name = "Опция автомобиля"
        verbose_name_plural = "Опции автомобилей"
        unique_together = ['car', 'feature']
    
    def __str__(self):
        return f"{self.car} - {self.feature}"