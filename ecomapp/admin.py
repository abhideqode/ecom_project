from django.contrib import admin
from .models import User, Product, WishItems,Wishlist


class CustomAdmin(admin.ModelAdmin):
    list_display = ('user_type', 'gender',)


admin.site.register(User, CustomAdmin)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(WishItems)