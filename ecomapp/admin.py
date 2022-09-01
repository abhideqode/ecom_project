from django.contrib import admin
from .models import User, Product, WishItems,Wishlist,CartItems,MyOrders


class CustomAdmin(admin.ModelAdmin):
    list_display = ('user_type', 'username',)


admin.site.register(User, CustomAdmin)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(WishItems)
admin.site.register(CartItems)
admin.site.register(MyOrders)