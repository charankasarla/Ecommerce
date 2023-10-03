from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product,BoughtProduct
from .serializers import ProductSerializer, UserRegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework import filters
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.shortcuts import redirect
#import request
# Create your views here.

class ProductListCreateView(APIView):
    #serializer_class = serializers.ProductSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        #print(serializer.data)
        filter_backends = (filters.SearchFilter,)
        search_fields = ('name',)
        return Response(serializer.data)

    def post(self, request,format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = Product(
                name=serializer.validated_data['name'],
                description=serializer.validated_data['description'],
                price=serializer.validated_data['price'],
                #quantity=serializer.validated_data['quantity'],
                # Add any other fields as needed
            )
            product.save()
            #print(serializer.data)
            response_serializer = ProductSerializer(product)

            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


''''class UserLoginView(APIView):
    #serializer_class = serializers.CustomerProfileSerializer
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('products/')
            #return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)'''

class ProductSearchView(APIView):
    def get(self, request):
        search_query = self.request.query_params.get('search', '')
        products = Product.objects.filter(name__icontains=search_query)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductSortView(APIView):
    def get(self, request):
        sort_order = self.request.query_params.get('sort', 'name')  # Default to sorting by name
        products = Product.objects.order_by(sort_order)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductFilterView(APIView):
    def get(self, request):
        category = self.request.query_params.get('category', '')
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BuyProductView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    def post(self, request, product_id):
        # Add the product to the customer's "bought" list
        product = get_object_or_404(Product, id=product_id)
        BoughtProduct.objects.create(customer=request.user, product=product)
        return Response({'message': 'Product bought successfully'}, status=status.HTTP_201_CREATED)

class BoughtProductListView(APIView):
    def get(self, request):
        # Filter BoughtProduct objects by the logged-in user (customer)
        bought_products = BoughtProduct.objects.filter(customer=request.user)

        # Retrieve the associated products
        products = [bought.product for bought in bought_products]

        # Serialize the products
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('../products/')
            return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Perform user logout by invalidating the authentication token
        request.session.clear()
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
