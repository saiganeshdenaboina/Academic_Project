from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views

urlpatterns = [
    # Admin Panel URL
    path("admin/", admin.site.urls),

    # Include URLs from the accounts app for authentication
    path('accounts/', include('accounts.urls')),   # This includes the URLs defined in the 'accounts' app
    
    # Other app URLs
    path("customers/", include("customers.urls")),
    path("products/", include("products.urls")),
    path("orders/", include("orders.urls")),
    path("payments/", include("payments.urls")),
    path("logistics/", include("logistics.urls")),
    path("vendors/", include("vendors.urls")),
    path("adminpanel/", include("adminpanel.urls")),  # Custom admin panel URLs
    path("reviews/", include("reviews.urls")),  # New reviews app URLs
    path("cart/", include("cart.urls", namespace='cart')),  # Include the cart app's URLs

    # Root URL for Home Page 
    path("", views.home, name="home"),  # Home page

    # Accounts login and dashboard URLs
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/logout/', views.user_logout, name='logout'),
    path('accounts/admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('accounts/customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('accounts/orders/', views.order_list, name='order_list'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
