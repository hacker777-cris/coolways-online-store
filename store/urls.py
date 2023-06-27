from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from store.views import payment_success_view, categories_view,home_view,signup_view,checkout_view,login_view,products_view,profile,addProduct,logoutuser,cart,add_to_cart,singleproduct_view
from payments.views import initiate_payment,payment_callback
urlpatterns = [
    path('',home_view,name = 'home'),
    path('signup',signup_view,name='signup'),
    path('checkout',checkout_view,name='checkout'),
    path('login',login_view,name='login'),
    path('logout',logoutuser, name = 'logout'),
    path('products',products_view,name='products'),
    path('categories', categories_view , name='categories'),
    path('singleproduct/<int:product_id>/', singleproduct_view,name='singleproduct'),
    path('add-to-cart/<int:product_id>/',add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('profile',profile, name = 'profile'),
    path('addproduct',addProduct, name='addproduct'),
    path('payments/initiate/', initiate_payment, name='initiate_payment'),
    path('payment_success',payment_success_view,name='payment_success'),
    path('payments/callback/', payment_callback, name='payment_callback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)