from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r"menu-items", views.MenuItemsView, basename = 'menu-items')
router.register(r"order", views.OrderView, basename= "order")
router.register(r"cart", views.CartView, basename= "cart")
router.register(r"order-items", views.OrderItemView, basename= "order-items")
router.register(r"category", views.CategoryView, basename= "category")
urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('users/', views.create_new_user),
    path('groups/manager/users/', views.get_managers),
]



