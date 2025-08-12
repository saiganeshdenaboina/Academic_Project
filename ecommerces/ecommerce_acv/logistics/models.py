from django.db import models
from django.apps import apps  # ✅ Avoid circular import
from accounts.models import CustomUser

# 🔹 Warehouse Model
class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField(default=0)  # Added a default value for capacity

    def __str__(self):
        return f"{self.name} ({self.location})"

# 🔹 Shipment Model
class Shipment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
    ]
    
    order = models.OneToOneField("orders.Order", on_delete=models.CASCADE, related_name="shipment")  # ✅ Use string reference
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    tracking_number = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return f"Shipment {self.id} - {self.status}"

    def get_order(self):
        """Fetch the Order object dynamically to avoid circular import issues."""
        Order = apps.get_model("orders", "Order")  # ✅ Correct way to avoid import issues
        return Order.objects.get(id=self.order_id)

# 🔹 Fleet Model 
class Fleet(models.Model):
    vehicle_name = models.CharField(max_length=255)
    license_plate = models.CharField(max_length=20, unique=True)
    capacity = models.IntegerField()
    assigned_driver = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={"role__name": "Logistics"}
    )

    def __str__(self):
        return f"{self.vehicle_name} ({self.license_plate})"
