from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('cars/', views.CarListView.as_view(), name='car-list'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car-detail'),
    path('cars/masked/', views.masked_cars_list, name='masked-cars-list'),
    path('cars/masked/<int:pk>/', views.masked_car_detail, name='masked-car-detail'),
]