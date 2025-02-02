from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import MenuItem, Order, Cart, OrderItem, Category
from .serializers import MenuItemSerializers, OrderSerializers, CartSerializers, OrderItemSerializers, CategorySerializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsManagerOnly, IsManagerDeliverycrewOwner
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.contrib.auth.models import User






class MenuPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param  = 'perpage'
    max_page_size = 3
    
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    
    
class MenuItemsView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsManagerOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # Collect all the menuitems
    queryset = MenuItem.objects.all()
    # Serialize all the menuitem
    serializer_class = MenuItemSerializers
    # Paginate API output
    pagination_class = MenuPagination
    # Enable filtering, seraching and ordering functionality
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category']
    ordering_fields = ['id', 'price']
    search_fields = ['title', 'category__title']
    
    
class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializers
    permission_classes = [IsAuthenticated]
    
class OrderView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsManagerDeliverycrewOwner]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    
    
class OrderItemView(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializers
    
@api_view(['POST'])
@permission_classes([AllowAny])
def create_new_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    if not username or not password or not email:
        return Response(
            {'error':'Please provide valid credentials'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        return Response(
            {'message':'User created successfully'},
            status=status.HTTP_201_CREATED
        )
    except:
        return Response(
            {'error':'Unable to create user'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
# /api/users/users/me/
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import serializers

# /api/groups/manager/users
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsManagerOnly])
def get_managers(request):
    if request.method == 'GET':
        if request.user.groups.filter(name='Manager').exists():
            managers = User.objects.filter(groups__name="Manager")
            manager_data = [
                {'id': manager.id, 'username':manager.username, 'email':manager.email} for manager in managers
            ]
            return Response({'managers': manager_data})
        
        return Response(
            {'error':'You do not have access to view this page'}, status=status.HTTP_403_FORBIDDEN
        )