from django.contrib import admin
from .models import Supplier, Seller, Container, Item

admin.site.register(Supplier)
admin.site.register(Seller)
admin.site.register(Container)
admin.site.register(Item)
