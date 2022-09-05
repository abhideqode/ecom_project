from django.contrib import admin
from .models import User, Product, WishItems, Wishlist, CartItems, MyOrders, Variations


class CustomAdmin(admin.ModelAdmin):
    list_display = ('user_type', 'username',)


class VariationsAdmin(admin.TabularInline):
    model = Variations


class ProductAdmin(admin.ModelAdmin):
    inlines = [VariationsAdmin, ]


admin.site.register(Product,ProductAdmin)

admin.site.register(User, CustomAdmin)
admin.site.register(Wishlist)
admin.site.register(WishItems)
admin.site.register(CartItems)
admin.site.register(MyOrders)
admin.site.register(Variations)
