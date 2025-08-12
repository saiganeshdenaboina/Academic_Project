from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Warehouse, Shipment, Fleet
from .forms import WarehouseForm, ShipmentForm, FleetForm
from accounts.decorators import role_required

# 🔹 Logistics Dashboard
@login_required
@role_required("Logistics")
def logistics_dashboard(request):
    return render(request, "logistics/logistics_dashboard.html")

# 🔹 Warehouse  Management
@login_required
@role_required("Logistics")
def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    return render(request, "logistics/warehouse_list.html", {"warehouses": warehouses})

@login_required
@role_required("Logistics")
def add_warehouse(request):
    if request.method == "POST":
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Warehouse added successfully!")
            return redirect("warehouse_list")
    else:
        form = WarehouseForm()
    return render(request, "logistics/add_warehouse.html", {"form": form})

@login_required
@role_required("Logistics")
def edit_warehouse(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == "POST":
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            messages.success(request, "Warehouse updated successfully!")
            return redirect("warehouse_list")
    else:
        form = WarehouseForm(instance=warehouse)
    return render(request, "logistics/edit_warehouse.html", {"form": form, "warehouse": warehouse})

# 🔹 Shipment Tracking
@login_required
@role_required("Logistics")
def shipment_list(request):
    shipments = Shipment.objects.all()
    return render(request, "logistics/shipment_list.html", {"shipments": shipments})

@login_required
@role_required("Logistics")
def update_shipment_status(request, shipment_id, status):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    shipment.status = status
    shipment.save()
    messages.success(request, f"Shipment status updated to {status}!")
    return redirect("shipment_list")

# 🔹 Fleet Management
@login_required
@role_required("Logistics")
def fleet_list(request):
    fleet = Fleet.objects.all()
    return render(request, "logistics/fleet_list.html", {"fleet": fleet})

@login_required
@role_required("Logistics")
def add_vehicle(request):
    if request.method == "POST":
        form = FleetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle added successfully!")
            return redirect("fleet_list")
    else:
        form = FleetForm()
    return render(request, "logistics/add_vehicle.html", {"form": form})
