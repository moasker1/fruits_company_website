from django.contrib import admin
from .models import Supplier, Seller, Container, Item, ContainerItem
from django.db.models import Sum

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'place', 'his_money', 'on_him_money', 'total','num_of_containers')  # Display the 'total' field in admin panel

@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    readonly_fields = ('num_of_items','main_total_count')
    
admin.site.register(Seller)
admin.site.register(Item)
admin.site.register(ContainerItem)
