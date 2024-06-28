from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from store.models import Product, Category
from .serializers import ProductSerializer


class GetProducts(APIView):
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
    def get(self, request):
        try:
            id = request.query_params.get("id")
            print("This is product id ", id)
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
