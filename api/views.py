from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from store.models import Product
from .serializers import ProductSerializer


class GetProducts(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"success": True, "data": serializer.data})


class GetProduct(APIView):
    def get(self, request):
        id = request.query_params.get("id")
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return Response({"success": True, "data": serializer.data})
