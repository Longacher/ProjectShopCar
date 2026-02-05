# config/urls.py
from django.contrib import admin
from django.urls import path, include
from cars import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('cars.urls')),  # API маршруты
    # Прямые маршруты для доступа через браузер
    path('cars/', views.CarListView.as_view(), name='car-list'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car-detail'),
    path('cars/masked/', views.masked_cars_list, name='masked-cars-list'),
    path('cars/masked/<int:pk>/', views.masked_car_detail, name='masked-car-detail'),
]
