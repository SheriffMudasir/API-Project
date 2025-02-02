from .models import MenuItem, Category, Cart, Order, OrderItem
from rest_framework import serializers
import bleach

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
        
        
class MenuItemSerializers(serializers.ModelSerializer):
    
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title'])
        if (attrs['price'] < 0):
            raise serializers.ValidationError('Price cannot be less than 0')
        return super().validate(attrs)
        
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']
        
        
        
        
class CartSerializers(serializers.ModelSerializer):

    # Use MenuItemSerializers to serialize the menu item details
    menuitem = MenuItemSerializers()

    class Meta:
        model = Cart
        fields = ['id', 'menuitem', 'quantity']
        
        
class OrderSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    delivery_crew = serializers.StringRelatedField()
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
        
        
class OrderItemSerializers(serializers.ModelSerializer):
    order = OrderSerializers() 
    menuitem = MenuItemSerializers() 
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']
