from django.contrib import admin
from .models import TBUsers
# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    list_display = ('user_id','password', 'user_name','phone_number','user_level')


admin.site.register(TBUsers, UsersAdmin)
