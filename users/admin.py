from django.contrib import admin
from .models import TBUsers
# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name')


admin.site.register(TBUsers, UsersAdmin)
