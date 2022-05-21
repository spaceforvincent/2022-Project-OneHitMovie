#Custom User 모델 등록
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class UserAdmin(admin.ModelAdmin):
    exclude = ('followings',)

admin.site.register(User, UserAdmin)