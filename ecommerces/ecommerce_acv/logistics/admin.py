from django.contrib import admin
from .models import Warehouse, Shipment, Fleet

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "capacity"]
    search_fields = ["name", "location"]

class ShipmentAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "warehouse", "status", "tracking_number"]
    list_filter = ["status"]
    search_fields = ["tracking_number"]

class FleetAdmin(admin.ModelAdmin):
    list_display = ["vehicle_name", "license_plate", "capacity", "assigned_driver"]
    search_fields = ["vehicle_name", "license_plate"]

admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(Fleet, FleetAdmin)

