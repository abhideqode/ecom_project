from django.urls import path
from . import views

app_name = 'ecomapp'
urlpatterns = [
    path('/dashboard/', views.test, name='ecomdash'),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('shopregister/', views.shopuser, name="shop_user"),
    path('approve/<str:pk>/', views.shopuserApp, name="approve_user"),
    path('requestlist/', views.requestlist, name="request_list"),
    path('shoplist/', views.shoplist, name="shop_list"),
    path('creatshopuser/', views.createshopuser, name="create_shop"),
    path('deleteshopuser/<str:pk>/', views.shopdelete, name="shop_delete"),
    path('addproduct/', views.addproduct, name="add_product"),
    path('listproduct/', views.list_product, name="list_product"),
    path('deleteproduct/<str:pk>/', views.productdelete, name="delete_product"),
    path('dupdateproduct/<str:pk>/', views.updateproduct, name="update_product"),
]
