from django.shortcuts import render, get_object_or_404
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
from django.contrib.auth.models import User, Group
from decimal import Decimal







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


# /api/groups/manager/users
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated, IsManagerOnly])
def get_managers(request, pk=None):
    if request.method == 'GET':
        if request.user.groups.filter(name='Manager').exists():
            if pk:
                try:
                    manager = User.objects.get(id=pk, groups__name="Manager")
                    manager_data = {
                        'id': manager.id,
                        'username':manager.username,
                        'email':manager.email
                    }
                    return Response({'manager': manager_data})
                except User.DoesNotExist:
                    return Response(
                        {'error':'Manager not fount'}, status=status.HTTP_404_NOT_FOUND
                    )
            else:
                managers = User.objects.filter(groups__name="Manager")
                manager_data = [
                    {'id': manager.id, 'username':manager.username, 'email':manager.email} for manager in managers
                ]
                return Response({'managers': manager_data})
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if not username or not password:
            return Response(
                {'error': 'Please provide username, password and email'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user, created = User.objects.get_or_create(username=username, defaults={'email': email})
            if created:
                user.set_password(password)
                user.save()
            manager_group = Group.objects.get(name='Manager')  
            user.groups.add(manager_group)
            return Response(
                {'success': 'User assigned to manager group successfully'}, 
                status=status.HTTP_201_CREATED
            )
        except Group.DoesNotExist:
            return Response(
                {'error': 'Manager group does not exist'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'User cannot be added currently. Try again!'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    if request.method == 'DELETE':
        if request.user.groups.filter(name='Manager').exists():
            if pk:
                try:
                    user = get_object_or_404(User, id=pk)
                    manager = Group.objects.get(name='Manager')
                    user.groups.remove(manager)
                    return Response(
                        {'sucess':'user removed from manager group'}, status=status.HTTP_201_CREATED
                    )
                except User.DoesNotExist:
                    return Response(
                        {'error': 'user does not exist as a manger'}, status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {'error': 'Please provide a userID to remove'}, status=status.HTTP_400_BAD_REQUEST
                )
    return Response(
            {'error':'You do not have access to view this page'}, status=status.HTTP_403_FORBIDDEN
        )
    
# /api/groups/delivery-crew/users
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated, IsManagerOnly])
def get_delivery_crews(request, pk=None):
    if request.method == "GET":
        if request.user.groups.filter(name='Manager').exists():
            if pk:
                try:
                    delivery_crew = User.objects.get(id=pk, groups__name='Delivery Crew')
                    delivery_crew_data = {
                        'id': delivery_crew.id,
                        'username': delivery_crew.username,
                        'email': delivery_crew.email
                    }
                    return Response({'delivery crew': delivery_crew_data})
                except User.DoesNotExist:
                    return Response({"error": "User does not exist i delivery crew list"}, status=status.HTTP_404_NOT_FOUND)
            else:
                delivery_crews = User.objects.filter(groups__name = 'Delivery Crew')
            delivery_crew_data = [
                {
                    'id': delivery_crew.id,
                    'username':delivery_crew.username,
                    'email':delivery_crew.email} for delivery_crew in delivery_crews
                ]
            return Response({'delivery crews': delivery_crew_data})
        return Response(
            {'error': 'You  donot have permission to view delivery crew list'}, status=status.HTTP_403_FORBIDDEN
        )
    if request.method == "POST":
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if not username or not password:
            return Response(
                {'error': 'Please provide a username and password'}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            delivery_crew_group, _ = Group.objects.get_or_create(name="Delivery Crew")
            user, created = User.objects.get_or_create(username=username, defaults={'email':email})
            if created:
                user.set_password(password)
                user.save()
            user.groups.add(delivery_crew_group)
            return Response(
                {'success':'user assigned to delivery crew successfully'}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
    if request.method == 'DELETE':
        if request.user.groups.filter(name='Manager').exists():
            if pk:
                delivery_crew_group = Group.objects.get(name='Delivery Crew')
                user = get_object_or_404(User, id=pk)
                if not user.groups.filter(name="Delivery Crew").exists():
                    return Response({'error':'User is not a delivery crew member'}, status=status.HTTP_404_NOT_FOUND)
                user.groups.remove(delivery_crew_group)
                return Response(
                    {'success': 'User has been removed from delivery crew successfully'}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error':'Please provide user id to be removed'}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {'error': 'You do not have permission to remove delivery crew members'}, 
            status=status.HTTP_403_FORBIDDEN
        )
        
        
        
# /api/cart/menu-items
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart_items(request):
    if request.method == 'GET':
        try:
            cart_content = Cart.objects.filter(user=request.user)
            if cart_content.exists():
                serializer = CartSerializers(cart_content, many=True)
                return Response({'items': serializer.data}, status=status.HTTP_200_OK)
            return Response({'message': 'Cart is empty'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
    elif request.method == 'POST':
        menuitem_id = request.data.get('menuitem')
        quantity = int(request.data.get('quantity', 1)) 
        
        if not menuitem_id:
            return Response(
                {'error': 'menuitem ID is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            menuitem = MenuItem.objects.get(id=menuitem_id)
            unit_price = menuitem.price
            price = unit_price * Decimal(str(quantity)) 
            
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                menuitem=menuitem,
                defaults={
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'price': price
                }
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.price = cart_item.unit_price * Decimal(str(cart_item.quantity))
                cart_item.save()
                
            return Response({'message': 'Item added to cart'}, status=status.HTTP_201_CREATED)
            
        except MenuItem.DoesNotExist:
            return Response(
                {'error': f'MenuItem with id {menuitem_id} does not exist'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to add item to cart: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    elif request.method == 'DELETE':
        try:
            Cart.objects.filter(user=request.user).delete()
            return Response({'message': 'Cart emptied'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)