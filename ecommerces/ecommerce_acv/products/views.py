from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib import messages

from .models import Product
from inventory.models import Inventory
from .forms import ProductForm

User = get_user_model()


# 🔹 Product List View
@login_required
def product_list(request):
    """Display the list of available products for customers & vendors."""
    products = Product.objects.filter(is_active=True, approval_status="Approved")  # Only show approved & active

    # Determine dashboard redirect based on user role
    dashboard_url = "customer_dashboard"
    if hasattr(request.user, "is_vendor") and request.user.is_vendor():
        dashboard_url = "vendor_dashboard"

    return render(request, "products/product_list.html", {
        "products": products,
        "dashboard_url": dashboard_url,
    })


# 🔹 Product Detail View
@login_required
def product_detail(request, product_id):
    """Display details of a single product (Only Approved & Active)."""
    product = get_object_or_404(Product, id=product_id, is_active=True, approval_status="Approved")
    return render(request, "products/product_detail.html", {"product": product})


# 🔹 Inventory View (Optional: This is better suited to `vendors/views.py`)
@login_required
def inventory_view(request):
    """Vendor's inventory view (moved here by mistake — better in vendors app)."""
    if not hasattr(request.user, "is_vendor") or not request.user.is_vendor():
        return render(request, "403.html")  # Optional: restrict non-vendors

    inventory_items = Inventory.objects.filter(product__vendor=request.user)
    return render(request, 'vendors/inventory.html', {'products': inventory_items})


# 🔹 Product Management View
def product_management(request):
    # Fetch all products to display in the product management page
    products = Product.objects.filter(is_approved=False, is_rejected=False)
    approved_products = Product.objects.filter(is_approved=True)
    return render(request, 'products/product_management.html', {
        'products': products,
        'approved_products': approved_products
    })


# 🔹 Add Product View
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)  # Do not save to the database yet
            product.vendor = request.user  # Set the vendor to the logged-in user
            product.save()  # Save the product to the database
            messages.success(request, 'Product added successfully!')
            return redirect('product_management')
        else:
            messages.error(request, 'Failed to add product. Please check the form for errors.')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})


# 🔹 Edit Product View
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()
        return redirect('product_management')
    return render(request, 'products/edit_product.html', {'product': product})


# 🔹 Delete Product View
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_management')


# View Product Details
def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'accounts/view_product.html', {'product': product})


# 🔹 Approve Product View
def approve_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_approved = True
    product.is_rejected = False
    product.approval_status = "Approved"
    product.save()
    messages.success(request, f"Product '{product.name}' has been approved.")
    return redirect('product_management')


# 🔹 Reject Product View
def reject_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_approved = False
    product.is_rejected = True
    product.approval_status = "Rejected"
    product.save()
    messages.success(request, f"Product '{product.name}' has been rejected.")
    return redirect('product_management')
