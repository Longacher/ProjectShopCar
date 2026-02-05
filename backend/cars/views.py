# views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Car
from .serializers import PublicCarSerializer, MaskedCarSerializer, FullCarSerializer

class CarListView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    
    def get_serializer_class(self):
        if self.request.query_params.get('full'):
            return FullCarSerializer
        return PublicCarSerializer

class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    
    def get_serializer_class(self):
        if self.request.query_params.get('full'):
            return FullCarSerializer
        return PublicCarSerializer

@api_view(['GET'])
def masked_cars_list(request):
    cars = Car.objects.all()
    masked_data = [car.get_masked_data() for car in cars]
    return Response(masked_data)

@api_view(['GET'])
def masked_car_detail(request, pk):
    try:
        car = Car.objects.get(pk=pk)
        return Response(car.get_masked_data())
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
