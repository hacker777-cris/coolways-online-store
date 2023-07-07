import stripe
from django.conf import settings
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.db.models import Q
from store.sign_upform import SignupForm
from store.models import Product,UserProfile,Cart,CartItem,Category,Order,OrderItem
from store.addproductform import ProductForm
# Create your views here.
stripe.api_key = 'sk_test_51NNYXvEifafv1oQMU0qOz9DrfLNNB5WG2jnHAzxmizAdUHU7T1Yk4EfUshB5A5fCNZBRCrB1Vk2P5N272Frgmd3E00UqN7mPbn'
def home_view(request):
     
     
     q = request.GET.get('q') if request.GET.get('q') != None else ''
     products = Product.objects.filter(
        Q(name__icontains=q) 
        )
    #products = Product.objects.all()  # Retrieve all products (or use a specific queryset)
     categories = Category.objects.all()

     context = {
        'categories':categories,
        'products': products
     }
     return render(request, 'home.html', context)


def signup_view(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('store:login')
    else:
        form = UserCreationForm()
    
    context =  {
        'form': form
        }
    
    return render(request, 'signup.html',context)
@login_required
def checkout_view(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    total_price = cart.get_total_price()

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if payment_method == 'online':
            # Process online payment using Stripe or your preferred payment gateway
            token = request.POST.get('stripeToken')
            charge = stripe.Charge.create(
                amount=int(total_price * 100),
                currency='usd',
                description='Online Store Purchase',
                source=token,
            )
            return redirect('store:payment_success')
        elif payment_method == 'delivery':
            delivery_location = request.POST.get('delivery_location')  # Get the delivery location from the request
            # Create an order with pay on delivery option
            order = Order.objects.create(user=user, total_price=total_price, payment_method='delivery', delivery_location=delivery_location)
            for cart_item in cart.cartitem_set.all():
                product = cart_item.product
                quantity = cart_item.quantity
                OrderItem.objects.create(order=order, product=product, quantity=quantity)

        # Clear the cart after successful payment or order creation
        cart.products.clear()

        return redirect('store:ordersuccess')

    context = {
        'cart': cart,
        'total_price': total_price,
        'stripe_publishable_key': 'pk_test_51NNYXvEifafv1oQM5tUCoYE2QEtO2xooQVb5RsbQORoL2ZT7KnaBHnIqAdub6XFZT5I4o8xQOE3fT1c1jJVAJHP40047JNNd62',
    }

    return render(request, 'checkout.html', context)

def order_success_view(request):

    return render(request,'ordersuccess.html',{})
def payment_success_view(request):
    # Logic for payment success
    return render(request, 'payment_success.html')


def login_view(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

        except:
             messages.error(request, 'user does not exist!!!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store:home')
            messages.success(request, 'Login Successful')
        else:
            messages.error(request, 'Username or Password is incorrect!!!')


    context = {
        'page':page
        
    }
    
    return render(request,'login.html',context)


def logoutuser(request):
    logout(request)
    return redirect('store:home')

def products_view(request):
    products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(request, 'products.html', context)

def categories_view(request):
    categories = Category.objects.all()

    context = {
        'categories':categories
    }
    return render(request, 'category.html',context)

def singleproduct_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    context = {
        'product': product
    }
    return render(request, 'singleproduct.html', context)

@login_required(login_url='store:login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('store:cart')



@login_required(login_url='store:login')
def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.cartitem_set.all()
    total_price = cart.get_total_price()
    
    return render(request, 'cart.html', {'cart': cart, 'items': items, 'total_price': total_price})

@login_required(login_url='store:login')
def profile(request):
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None
    
    completed_orders = Order.objects.filter(user=user, payment_method='online')
    pay_on_delivery_orders = Order.objects.filter(user=user, payment_method='delivery')
    

    context = {
        'user': user,
        'profile': profile,
        'completed_orders':completed_orders,
        'pay_on_delivery_orders':pay_on_delivery_orders
    }
    return render(request, 'profile.html', context)



@login_required(login_url='login')
def addProduct(request):
    if not request.user.is_superuser:
        # Handle unauthorized access
        return HttpResponseForbidden("You are not authorized to access this page.")
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = ProductForm()
    context = {
        'form':form
    }
        
    return render(request, 'addproduct.html',context)
