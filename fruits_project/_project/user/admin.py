from django.contrib import admin
from .models import Supplier, Seller, Container, Item

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'place', 'his_money', 'on_him_money', 'total')  # Display the 'total' field in admin panel

admin.site.register(Seller)
admin.site.register(Container)
admin.site.register(Item)