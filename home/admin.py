from django.contrib import admin
from home.models import Profile, Post, Comment
from django.contrib.auth.models import User

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin





# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
