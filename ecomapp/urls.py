from django.urls import path
from . import views

app_name = 'ecomapp'
urlpatterns = [
    path('/dashboard/', views.test, name='ecomdash'),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('shopregister/', views.shopuser, name="shop_user"),
    path('approve/<str:pk>/', views.shopuserApp, name="approve_user"),
    path('requestlist/', views.requestlist, name="request_list"),
]