from django.contrib import admin
from .models import User


class CustomAdmin(admin.ModelAdmin):
    list_display = ('user_type', 'gender',)


admin.site.register(User, CustomAdmin)
