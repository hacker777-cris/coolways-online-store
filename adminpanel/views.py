from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from store.models import Cart, CartItem, Product, Category, UserProfile, Order, OrderItem

def admin_dashboard(request):
    # Logic for admin dashboard
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_users = UserProfile.objects.count()
    total_orders = Order.objects.count()
    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_users': total_users,
        'total_orders': total_orders
    }
    return render(request, 'admin_panel/dashboard.html', context)

def admin_product_view(request):
    products = Product.objects.all()

    context = {
        'products':products
    }

    return render(request, 'admin_panel/adminproducts.html', context)

def admin_carts(request):
    # Logic for managing carts
    carts = Cart.objects.all()
    context = {
        'carts': carts
    }
    return render(request, 'admin_panel/carts.html', context)

def admin_view_carts(request, cart_id):
    # Logic for managing carts
    carts = Cart.objects.get(id=cart_id)
    context = {
        'carts': carts
    }
    return render(request, 'admin_panel/view_carts.html', context)

def admin_products(request):
    # Logic for managing products
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'admin_panel/products.html', context)

def admin_product_detail(request, product_id):
    # Logic for viewing details of a specific product
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'admin_panel/product_detail.html', context)

# Add more views as needed for other admin functionality

def admin_orders_view(request):
    orders = Order.objects.all()

    context = {
        'orders':orders

    }

    return render(request,'admin_panel/orders.html',context)

def single_order_view(request, order_id):
    print("Entering single_order_view")
    user_order = Order.objects.get(id=order_id)
    print("user_order:", user_order)
    products = user_order.products.all()
    print("products:", products)
    context = {
        'user_order': user_order,
        'products': products
    }

    return render(request, 'admin_panel/single_order.html', context)



