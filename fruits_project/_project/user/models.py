from django.db import models
from django.utils import timezone


class Supplier(models.Model):
    name = models.CharField(max_length=30)
    place = models.CharField(max_length=70, default='غير محدد')
    date_created = models.DateField(default=timezone.now().date())
    
    def __str__(self) -> str:
        return self.name