from django.db import models
from django.utils import timezone
from django.db.models import Sum

class Supplier(models.Model):
    name = models.CharField(max_length=30)
    place = models.CharField(max_length=70, default='غير محدد')
    date = models.DateField(default=timezone.now().date())
    type = models.CharField(max_length=30, default='عمولة')
    his_money = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    on_him_money = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    num_of_containers = models.PositiveIntegerField(default=0)
    
    @property
    def total(self):
        return self.his_money - self.on_him_money
    
    @property  
    def num_of_containers(self):
        return self.container_set.count()
    
    def __str__(self):
        return self.name
# ===================================================================================================
class Seller(models.Model):
    name = models.CharField(max_length=30)
    place = models.CharField(max_length=70, default='غير محدد')
    date = models.DateField(default=timezone.now().date())

    def __str__(self):
        return self.name
# ===================================================================================================
class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date = models.DateField(default=timezone.now().date())

    def __str__(self):
        return self.name
# ===================================================================================================
class Container(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    type = models.CharField(max_length=30, default='عمولة')
    num_sold_items = models.PositiveIntegerField(null=True)
    num_not_sold_items = models.PositiveIntegerField(null=True)

    @property
    def main_total_count(self):
        return self.containeritem_set.aggregate(total_count=Sum('count'))['total_count'] or 0

    @property
    def num_of_items(self):
        return self.containeritem_set.count()

    def __str__(self):
        return f"Container {self.id} - {self.date}"
# ===================================================================================================
class ContainerItem(models.Model):  
    container = models.ForeignKey(Container, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    tool = models.CharField(max_length=100, default="صناديق")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.id}-{self.item.name}"
# ===================================================================================================