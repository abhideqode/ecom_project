"""
    this admin.py contains all the models for the super user
"""
from django.contrib import admin
from .models import User, Product, WishItems, Wishlist, CartItems, MyOrders, Variations


class CustomAdmin(admin.ModelAdmin):
    """
        this custom admin models of the project
    """
    list_display = ('user_type', 'username',)


class VariationsAdmin(admin.TabularInline):
    """
        this variations admin of the project
    """
    model = Variations


class ProductAdmin(admin.ModelAdmin):
    """
        this  ProductAdmin of the project
    """
    inlines = [VariationsAdmin, ]


admin.site.register(Product, ProductAdmin)

admin.site.register(User, CustomAdmin)
admin.site.register(Wishlist)
admin.site.register(WishItems)
admin.site.register(CartItems)
admin.site.register(MyOrders)
admin.site.register(Variations)
