from django.urls import path
from .views import (
    logistics_dashboard, warehouse_list, add_warehouse,
    shipment_list, update_shipment_status, fleet_list, add_vehicle, edit_warehouse
)

app_name = 'logistics'  # Register the namespace for the logistics app

urlpatterns = [
    path("dashboard/", logistics_dashboard, name="logistics_dashboard"),

    # Warehouse Management
    path("warehouses/", warehouse_list, name="warehouse_list"),
    path("warehouses/add/", add_warehouse, name="add_warehouse"),
    path("warehouses/edit/<int:pk>/", edit_warehouse, name="edit_warehouse"),

    # Shipment Tracking 
    path("shipments/", shipment_list, name="shipment_list"),
    path("shipments/update/<int:shipment_id>/<str:status>/", update_shipment_status, name="update_shipment_status"),

    # Fleet Management
    path("fleet/", fleet_list, name="fleet_list"),
    path("fleet/add/", add_vehicle, name="add_vehicle"),
]
