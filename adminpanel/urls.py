from django.urls import path
from adminpanel import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('carts/', views.admin_carts, name='carts'),
    path('products/', views.admin_products, name='products'),
    path('products/<int:product_id>/', views.admin_product_detail, name='product_detail'),
    path('adminproducts', views.admin_product_view, name='adminproducts'),
    # Add more URL patterns for other admin views
]
