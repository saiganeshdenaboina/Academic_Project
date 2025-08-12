from django.urls import path
from . import views

app_name = 'logistics'  # Add this line to define the namespace

urlpatterns = [
    path('logistics/warehouses/', views.warehouse_list, name='warehouse_list'),
]