from django.contrib import admin
from .models  import Category, MenuItem, Cart, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ['title']
    
    
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'featured', 'category')
    list_filter = ('featured', 'category')
    search_fields = ['title']
    
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'menuitem', 'quantity', 'price')
    search_fields = ['user__username', 'menuitem__title']
    

    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'delivery_crew', 'status', 'total', 'date')
    search_fields = ['user__username', 'status']
    
    
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menuitem', 'quantity', 'price')
    search_fields = ['order__id', 'menuitem__title']
    