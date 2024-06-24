from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.GetProducts.as_view(), name="get_products"),
]
