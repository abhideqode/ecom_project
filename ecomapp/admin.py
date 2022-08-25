from django.contrib import admin
from .models import User, Product


class CustomAdmin(admin.ModelAdmin):
    list_display = ('user_type', 'gender',)


admin.site.register(User, CustomAdmin)
admin.site.register(Product)