from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.apps import apps  # For dynamic model import
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from products.models import Product
from .models import Order, OrderItem
from cart.models import Cart


# ✅ CUSTOMER PLACES AN ORDER
@login_required
def place_order(request):
    """Converts cart items to an order with stock deduction."""
    Cart = apps.get_model("cart", "Cart")
    cart_items = Cart.objects.filter(customer=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect("cart:view_cart")

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    try:
        with transaction.atomic():
            # Check and reduce stock
            for item in cart_items:
                product = item.product
                if product.current_stock < item.quantity:
                    raise ValueError(f"Not enough stock for {product.name}")
                product.reduce_stock(item.quantity)

            # Create Order
            order = Order.objects.create(
                customer=request.user,
                total_price=total_price,
                status="Pending"
            )

            # Create OrderItems
            order_items = [
                OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            cart_items.delete()  # Clear cart after successful order

        messages.success(request, "Order placed successfully! 🚀")
        return redirect("orders:order_list")

    except ValueError as e:
        messages.error(request, str(e))
        return redirect("cart:view_cart")


# ✅ CUSTOMER VIEWS ORDER LIST
@login_required
def order_list(request):
    orders = Order.objects.filter(customer=request.user).order_by("-order_date")
    return render(request, "orders/order_list.html", {"orders": orders})


# ✅ CUSTOMER VIEWS ORDER DETAILS
@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, "orders/order_details.html", {"order": order})


# ✅ CUSTOMER CANCELS PENDING ORDER
@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    if request.method == "POST":
        status = request.POST.get("status")
        if status == "Cancelled" and order.status == "Pending":
            order.status = "Cancelled"
            order.save()
            messages.success(request, "Order cancelled successfully!")
        else:
            messages.warning(request, "Order cannot be updated.")
        return redirect("orders:order_list")

    return render(request, "orders/update_order.html", {"order": order})


# ✅ CHECKOUT VIEW
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(customer=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect("cart:view_cart")

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        try:
            with transaction.atomic():
                for item in cart_items:
                    if item.product.current_stock < item.quantity:
                        raise ValueError(f"Not enough stock for {item.product.name}")
                    item.product.reduce_stock(item.quantity)

                order = Order.objects.create(
                    customer=request.user,
                    total_price=total_price,
                    status="Pending"
                )

                OrderItem.objects.bulk_create([
                    OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
                    for item in cart_items
                ])

                cart_items.delete()

            messages.success(request, "Order placed successfully!")
            return redirect("orders:order_list")

        except ValueError as e:
            messages.error(request, str(e))
            return redirect("cart:view_cart")

    return render(request, "orders/checkout.html", {"cart_items": cart_items})


# ✅ DOWNLOAD INVOICE
@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    response = HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = f'attachment; filename="invoice_{order.id}.txt"'
    response.write(f"Invoice for Order {order.id}\n")
    response.write(f"Customer: {order.customer.username}\n")
    response.write(f"Total Price: ${order.total_price}\n")
    response.write("Items:\n")
    for item in order.items.all():
        response.write(f"- {item.product.name}: {item.quantity} x ${item.price}\n")

    return response


# ✅ VENDOR ACCEPTS ORDER
@login_required
def vendor_accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, vendor=request.user)

    if order.status != "Pending":
        messages.warning(request, "This order cannot be accepted.")
        return redirect("vendors:order_list")

    order.status = "Accepted"
    order.save()
    messages.success(request, f"Order {order.id} is now accepted.")
    return redirect("vendors:order_list")


# ✅ VENDOR MARKS ORDER AS PACKAGED
@login_required
def vendor_pack_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, vendor=request.user)

    if order.status != "Accepted":
        messages.warning(request, "Order must be 'Accepted' before packaging.")
        return redirect("vendors:order_list")

    order.status = "Packaged"
    order.save()
    messages.success(request, f"Order {order.id} is now packaged.")
    return redirect("vendors:order_list")


# ✅ LOGISTICS TEAM SHIPS ORDER
@login_required
def logistics_ship_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, logistics_team=request.user)

    if order.status != "Packaged":
        messages.warning(request, "Order must be 'Packaged' before shipping.")
        return redirect("logistics:order_list")

    order.status = "Shipped"
    order.save()
    messages.success(request, f"Order {order.id} is now shipped.")
    return redirect("logistics:order_list")


# ✅ DELIVERY BOY MARKS AS DELIVERED
@login_required
def delivery_boy_deliver_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, delivery_boy=request.user)

    if order.status != "Out for Delivery":
        messages.warning(request, "Order is not ready for final delivery.")
        return redirect("delivery:order_list")

    order.status = "Delivered"
    order.save()
    messages.success(request, f"Order {order.id} delivered successfully!")
    return redirect("delivery:order_list")


# # orders/views.py

# from django.shortcuts import render
# from orders.models import OrderItem
# from products.models import Product

# orders/views.py 

from django.contrib.auth.decorators import login_required

@login_required
def all_orders_view(request):
    vendor = request.user
    products = Product.objects.filter(vendor=vendor)
    order_items = OrderItem.objects.filter(product__in=products).select_related('order', 'product')

    return render(request, 'orders/all_orders.html', {
        'order_items': order_items
    })


# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from logistics.models import Warehouse, Shipment
from .models import Order

def return_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status != "Delivered":
        messages.error(request, "Only delivered orders can be returned.")
        return redirect("order_detail", order_id=order.id)

    # Reverse flow
    order.status = "In Transit"
    order.is_returned = True
    order.current_warehouse = Warehouse.objects.first()  # Optional: Use closest/assigned warehouse
    order.save()

    Shipment.objects.create(
        order=order,
        warehouse=order.current_warehouse,
        status="Pending"
    )

    messages.success(request, f"Return initiated for Order #{order.id}.")
    return redirect("order_detail", order_id=order.id)


# ✅ VIEW ALL ORDERS
from django.shortcuts import render
from .models import Order

def view_orders(request):
    orders = Order.objects.all()
    return render(request, 'accounts/view_orders.html', {'orders': orders})


# ✅ UPDATE ORDER STATUS VIA POST REQUEST
@csrf_exempt
def update_order_status(request, order_id):
    if request.method == "POST":
        try:
            order = get_object_or_404(Order, id=order_id)
            data = json.loads(request.body)
            new_status = data.get("status")

            if new_status:
                order.status = new_status
                order.save()
                return JsonResponse({"success": True, "message": "Order status updated successfully."})
            else:
                return JsonResponse({"success": False, "message": "Invalid status."}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


# Order Management View
def order_management(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_management.html', {'orders': orders})

# View Order Details
def view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/view_order.html', {'order': order})

# Edit Order
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            return redirect('order_management')
    return render(request, 'orders/edit_order.html', {'order': order})

# Delete Order
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_management')
