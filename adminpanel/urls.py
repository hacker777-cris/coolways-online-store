from django.urls import path
from adminpanel import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('carts/', views.admin_carts, name='carts'),
    path('products/', views.admin_products, name='products'),
    path('products/<int:product_id>/', views.admin_product_detail, name='product_detail'),
    path('adminproducts', views.admin_product_view, name='adminproducts'),
    path('orders',views.admin_orders_view,name='orders'),
    path('single_order/<int:order_id>/',views.single_order_view,name='single_order'),
    path('viewcarts/<int:cart_id>/',views.admin_view_carts,name='viewcarts'),
    # Add more URL patterns for other admin views
]
