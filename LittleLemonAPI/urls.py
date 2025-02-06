from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r"menu-items", views.MenuItemsView, basename = 'menu-items')
router.register(r"category", views.CategoryView, basename= "category")
router.register(r"orders", views.OrderView, basename="orders")
urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('users/', views.create_new_user),
    path('groups/manager/users/', views.get_managers),
    path('groups/manager/users/<int:pk>/', views.get_managers),
    path('groups/delivery-crew/users/', views.get_delivery_crews),
    path('groups/delivery-crew/users/<int:pk>/', views.get_delivery_crews),
    path('cart/menu-items/', views.cart_items),
    path('cart/menu-items/<int:pk>/', views.cart_items),
]



