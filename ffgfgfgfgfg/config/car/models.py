from django.db import models

class Underwear(models.Model):
    GENDER_CHOICES = [
        ('men', 'Мужские'),
        ('women', 'Женские'),
        ('unisex', 'Унисекс'),
    ]

    TYPE_CHOICES = [
        ('briefs', 'Трусы-плавки'),
        ('boxers', 'Боксеры'),
        ('thong', 'Стринги'),
        ('bikini', 'Бикини'),
        ('high_cut', 'Хай-кат'),
        ('other', 'Другое'),
    ]

    name = models.CharField('Название', max_length=100)
    gender = models.CharField('Пол', max_length=10, choices=GENDER_CHOICES, default='unisex')
    underwear_type = models.CharField('Тип', max_length=20, choices=TYPE_CHOICES, default='briefs')
    material = models.CharField('Материал', max_length=100, help_text='Например: хлопок, полиэстер и т.д.')
    color = models.CharField('Цвет', max_length=50)
    size = models.CharField('Размер', max_length=10)  
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    in_stock = models.BooleanField('В наличии', default=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_gender_display()}, {self.get_underwear_type_display()})"

    class Meta:
        verbose_name = 'Трусы'
        verbose_name_plural = 'Трусы'