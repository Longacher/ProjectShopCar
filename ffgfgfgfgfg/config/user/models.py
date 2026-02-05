from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=15, verbose_name="телефон")
    email = models.CharField

    def mask_phone(self):
        if self.phone and '@' in self.email: 
            name,domain = self.email.split('@',1)
            return f"{name[0]}***@{domain}"
        return self.email
    

