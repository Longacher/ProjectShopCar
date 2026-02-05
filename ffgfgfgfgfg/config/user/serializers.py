from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from.models import User

class UserSerializer(serializers.ModelSerializer): 

    password = serializers.CharField(
        wrire_only = True, 
        required = True, 
        validators = [validate_password]

    )

    class Meta: 
        model = User 

        fields = ['id', 'username', 'email', 'phone', 'password']

        