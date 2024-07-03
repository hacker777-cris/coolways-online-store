from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from store.models import Product, Category, Cart, CartItem
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils.decorator import jwt_required


class GetProducts(APIView):
    @method_decorator(jwt_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetProduct(APIView):
    @method_decorator(jwt_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        try:
            id = request.query_params.get("id")
            if id is None:
                return Response(
                    {"success": False, "error": "Product ID not provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product)
            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        except Product.DoesNotExist:
            return Response(
                {"success": False, "error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetProductsByCategory(APIView):
    @method_decorator(jwt_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        try:
            category_name = request.query_params.get("category")
            if not category_name:
                return Response(
                    {"success": False, "error": "Category name not provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            category = Category.objects.get(name=category_name)
            products = Product.objects.filter(category=category)
            serializer = ProductSerializer(products, many=True)
            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        except Category.DoesNotExist:
            return Response(
                {"success": False, "error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetCart(APIView):
    @method_decorator(jwt_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        try:
            user = request.user
            cart = Cart.objects.get(user=user)
            products = cart.products
            serializer = ProductSerializer(products, many=True)
            return Response({"success": True, "data": serializer.data})
        except Cart.DoesNotExist:
            return Response(
                {"success": False, "error": "Cart not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AddToCart(APIView):
    @method_decorator(jwt_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            product_id = request.data.get("product_id")
            product = get_object_or_404(Product, id=product_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart, product=product
            )

            if not item_created:
                cart_item.quantity += 1
                cart_item.save()

            return Response({"success": True, "Message": "Item added to cart"})
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            return Response({"success": True, "Message": "User already logged in"})

        try:
            username = request.data.get("username").lower()
            password = request.data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "success": True,
                        "Message": "User logged in successfully",
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    }
                )
            else:
                return Response({"success": False, "Message": "Invalid credentials"})
        except User.DoesNotExist:
            return Response({"success": False, "Message": "User does not exist"})
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "Message": "User Created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
