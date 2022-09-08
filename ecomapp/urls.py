"""
    this urls.py contains all the urls of the project
"""
# from unicodedata import name
from django.urls import path
from . import views

app_name = 'ecomapp'
urlpatterns = [
    # path('dashboard/', views.test, name='ecomdash'),
    # path('update_order/<str:pk>/', views.update_order, name="update_order"),
    path('shopregister/', views.shop_user, name="shop_user"),
    # path('approve/<str:pk>/', views.shopuser_app, name="approve_user"),
    path('requestlist/', views.request_list, name="request_list"),
    # path('shoplist/', views.shop_list, name="shop_list"),
    # path('creatshopuser/', views.create_shopuser, name="create_shop"),
    # path('deleteshopuser/<str:pk>/', views.shop_delete, name="shop_delete"),
    # path('addproduct/', views.add_product, name="add_product"),
    # path('listproduct/', views.list_product, name="list_product"),
    # path('deleteproduct/<str:pk>/', views.product_delete, name="delete_product"),
    # path('dupdateproduct/<str:pk>/', views.update_product, name="update_product"),
    path('addtowishlist/<str:pk>/', views.add_to_wishlist, name="add_to_wishlist"),
    # path('gotowishlist/', views.go_to_wishlist, name="go_to_wishlist"),
    # path('removefromwishlist/<str:pk>/', views.remove_from_wishlist_function,
    #      name="remove_from_wishlist_function"),
    # path('filter/', views.filter, name="filter_product"),

    # path('shop_user/', views.newshop_user, name="shopuser_url"),
    path('addtocart/<str:pk>/<str:color>/<str:size>/', views.add_to_cart, name="add_to_cart"),
    path('gotocart/', views.go_to_cart, name="go_to_cart"),
    path('removefromcart/<str:pk>/', views.remove_from_cart_function,
         name="remove_from_wishlist_function"),

    # Myorders fuctions
    path('add_to_my_orders/', views.add_to_my_orders, name="add_to_myorders"),
    path('go_to_your_order/', views.go_to_your_order, name="go_to_your_order"),

    path('remove_from_order/<str:pk>/', views.remove_from_order, name="remove_from_order"),
    path('update_order_quantity/<str:pk>/<str:quantity>/',
         views.update_order_quantity, name="update_order_quantity"),
    # path('order_placed/',views.order_placed,name="order_placed"),
    path('shop_orders/', views.shop_orders, name="shop_orders"),

    path('final_address/', views.final_address, name="final_address"),
    path('list_product_admin/<str:pk>/', views.list_product_admin,
         name='list_product_admin'),
    path('shop_orders_admin/<str:pk>/', views.shop_orders_admin, name='shop_orders_admin'),
    path('all_customers_admin/', views.all_customers_admin, name='all_customers_admin'),
    path('go_to_your_order_admin/<str:pk>/', views.go_to_your_order_admin,
         name='go_to_your_order_admin'),
    path('product_sales/<str:pk>/<str:pk1>/', views.product_sales, name='product_sales'),

    # Class Based
    path('update_order/<str:pk>/', views.UpdateOrder.as_view(), name="update_order"),
    path('shop_user/', views.NewShopUser.as_view(), name="shopuser_url"),
    path('dashboard/', views.Test.as_view(), name="ecomdash"),
    path('approve/<str:pk>/', views.ShopUserRequest.as_view(), name="approve_user"),
    path('shoplist/', views.ShopList.as_view(), name="shop_list"),
    path('creatshopuser/', views.CreateShopUser.as_view(), name="create_shop"),
    path('addproduct/', views.AddProduct.as_view(), name="add_product"),
    path('listproduct/', views.ListProduct.as_view(), name="list_product"),
    path('deleteshopuser/<str:pk>/', views.ShopProductDelete.as_view(), name="shop_delete"),
    path('deleteproduct/<str:pk>/', views.ProductDelete.as_view(), name="delete_product"),
    path('dupdateproduct/<str:pk>/', views.UpdateProduct.as_view(), name="update_product"),
    path('gotowishlist/', views.GoToWishlist.as_view(), name="go_to_wishlist"),
    path('removefromwishlist/<str:pk>/', views.RemoveProductWishlist.as_view(),
         name="remove_from_wishlist_function"),
]
