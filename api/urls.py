from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.GetProducts.as_view(), name="get_products"),
    path("get-product/", views.GetProduct.as_view(), name="get_product"),
    path(
        "get-product-by-category/",
        views.GetProductsByCategory.as_view(),
        name="get-product-by-category",
    ),
    path("get-cart/", views.GetCart.as_view(), name="get-cart"),
    path("add-to-cart/", views.AddToCart.as_view()),
    path("login/", views.LoginView.as_view()),
    path("sign-up/", views.SignupView.as_view()),
]
