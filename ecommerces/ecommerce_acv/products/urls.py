from django.urls import path
from .views import product_list, product_detail, product_management, edit_product, delete_product, view_product, approve_product, reject_product, add_product

urlpatterns = [
    path("", product_list, name="product_list"),
    path("<int:product_id>/", product_detail, name="product_detail"),
    path("product-management/", product_management, name="product_management"),
    path('add-product/', add_product, name='add_product'),
    path('edit-product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('view-product/<int:product_id>/', view_product, name='view_product'),
    path('approve-product/<int:product_id>/', approve_product, name='approve_product'),
    path('reject-product/<int:product_id>/', reject_product, name='reject_product'),
]



